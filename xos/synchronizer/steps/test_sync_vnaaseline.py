
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest
from mock import patch, call, Mock, MagicMock, PropertyMock
import mock

import os, sys

test_path=os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
service_dir=os.path.join(test_path, "../../../..")
xos_dir=os.path.join(test_path, "../../..")
if not os.path.exists(os.path.join(test_path, "new_base")):
    xos_dir=os.path.join(test_path, "../../../../../../orchestration/xos/xos")
    services_dir=os.path.join(xos_dir, "../../xos_services")

# chosen to match https://github.com/opencord/ecord/blob/master/examples/vnaasglobal-service-reference.yaml
ONOS_NAME = "onfGlobalONOS"
ONOS_IP = "onos-cord"
ONOS_PORT = 8182
ONOS_USERNAME = "onos"
ONOS_PASSWORD = "rocks"
ONOS_TYPE = "global"

BWP_GOLD_CBS = 2000
BWP_GOLD_EBS = 2700
BWP_GOLD_CIR = 20000
BWP_GOLD_EIR = 5000
BWP_GOLD_NAME = "gold"

CONNECT_POINT_1_TENANT = "onf"
CONNECT_POINT_1_NAME = "uni1"
CONNECT_POINT_1_LATLNG = "[37.973535, -122.531087]"
CONNECT_POINT_1_CPE_ID = "domain:10.90.1.30-cord-onos/1"

CONNECT_POINT_2_TENANT = "onf"
CONNECT_POINT_2_NAME = "uni2"
CONNECT_POINT_2_LATLNG = "[37.773972, -122.431297]"
CONNECT_POINT_2_CPE_ID = "domain:10.90.1.30-cord-onos/1"

ELINE_VLANIDS = "100"
ELINE_NAME = "testeline"

class TestSyncvNaaSEline(unittest.TestCase):
    def setUp(self):
        global SyncvNaaSEline, MockObjectList

        self.sys_path_save = sys.path
        sys.path.append(xos_dir)
        sys.path.append(os.path.join(xos_dir, 'synchronizers', 'new_base'))

        config = os.path.join(test_path, "test_config.yaml")
        from xosconfig import Config
        Config.clear()
        Config.init(config, 'synchronizer-config-schema.yaml')

        from synchronizers.new_base.mock_modelaccessor_build import build_mock_modelaccessor
        build_mock_modelaccessor(xos_dir, services_dir, ["vnaas/xos/vnaas.xproto"])

        import synchronizers.new_base.modelaccessor
        import synchronizers.new_base.model_policies.model_policy_tenantwithcontainer
        import sync_vnaaseline
        from sync_vnaaseline import SyncvNaaSEline, model_accessor

        from mock_modelaccessor import MockObjectList

        # import all class names to globals
        for (k, v) in model_accessor.all_model_classes.items():
            globals()[k] = v

        # Some of the functions we call have side-effects. For example, creating a VSGServiceInstance may lead to creation of
        # tags. Ideally, this wouldn't happen, but it does. So make sure we reset the world.
        model_accessor.reset_all_object_stores()

        self.syncstep = SyncvNaaSEline()

        self.onosModel = OnosModel(name=ONOS_NAME,
                                   onos_ip=ONOS_IP,
                                   onos_port=ONOS_PORT,
                                   onos_username=ONOS_USERNAME,
                                   onos_password=ONOS_PASSWORD,
                                   onos_type=ONOS_TYPE)
        self.bandwidthProfile = BandwidthProfile(cbs=BWP_GOLD_CBS,
                                                 ebs=BWP_GOLD_EBS,
                                                 cir=BWP_GOLD_CIR,
                                                 eir=BWP_GOLD_EIR,
                                                 name=BWP_GOLD_NAME)
        self.connect_point_1 = UserNetworkInterface(tenant=CONNECT_POINT_1_TENANT,
                                                         name=CONNECT_POINT_1_NAME,
                                                         latlng=CONNECT_POINT_1_LATLNG,
                                                         cpe_id=CONNECT_POINT_1_CPE_ID)
        self.connect_point_2 = UserNetworkInterface(tenant=CONNECT_POINT_2_TENANT,
                                                         name=CONNECT_POINT_2_NAME,
                                                         latlng=CONNECT_POINT_2_LATLNG,
                                                         cpe_id=CONNECT_POINT_2_CPE_ID)

        self.eline = ELine(name=ELINE_NAME,
                           connect_point_1=self.connect_point_1,
                           connect_point_2=self.connect_point_2,
                           vlanids=ELINE_VLANIDS,
                           cord_site_name=ONOS_NAME,
                           bwp=self.bandwidthProfile)

    def tearDown(self):
        sys.path = self.sys_path_save

    def test_sync_record(self):
        with patch.object(BandwidthProfile.objects, "get_items") as bwp_objects, \
             patch.object(OnosModel.objects, "get_items") as onos_objects, \
             patch("requests.post") as requests_post:

            bwp_objects.return_value = [self.bandwidthProfile]
            onos_objects.return_value = [self.onosModel]

            requests_post.return_value = Mock(status_code=200)

            self.syncstep.sync_record(self.eline)

            requests_post.assert_called()

            attrs = requests_post.call_args[1]["data"]
            attrs = eval(attrs) # convert POST string back into a dict

            desired_attrs = {"evcCfgId": ELINE_NAME,
                             "eir": BWP_GOLD_EIR,
                             "cir": BWP_GOLD_CIR,
                             "uniList": [CONNECT_POINT_1_CPE_ID, CONNECT_POINT_2_CPE_ID],
                             "ebs": BWP_GOLD_EBS,
                             "vlanId": int(ELINE_VLANIDS),
                             "cbs": BWP_GOLD_CBS,
                             "evcId": ELINE_NAME,
                             "evcType": "POINT_TO_POINT"}

            self.assertDictContainsSubset(desired_attrs, attrs)

    def test_delete_record(self):
        with patch.object(BandwidthProfile.objects, "get_items") as bwp_objects, \
             patch.object(OnosModel.objects, "get_items") as onos_objects, \
             patch("requests.delete") as requests_delete:

            bwp_objects.return_value = [self.bandwidthProfile]
            onos_objects.return_value = [self.onosModel]

            requests_delete.return_value = Mock(status_code=200)

            self.syncstep.delete_record(self.eline)

            requests_delete.assert_called()

            url = requests_delete.call_args[0][0]
            self.assertEqual(url, "http://%s:%d/carrierethernet/evc/testeline" % (ONOS_IP, ONOS_PORT))

    def test_get_onos_global_addr(self):
        addr = self.syncstep.get_onos_global_addr(self.onosModel)
        self.assertEqual(addr, 'http://%s:%d/carrierethernet/evc' % (ONOS_IP, ONOS_PORT))

    def test_get_onos_global_auth(self):
        auth = self.syncstep.get_onos_global_auth(self.onosModel)
        self.assertEqual(auth.username, ONOS_USERNAME)
        self.assertEqual(auth.password, ONOS_PASSWORD)

if __name__ == '__main__':
    unittest.main()


