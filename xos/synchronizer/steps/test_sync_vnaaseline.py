
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

        self.onosModel = OnosModel(name="onfGlobalONOS",
                                   onos_ip="127.0.0.1",
                                   onos_port=8182,
                                   onos_username="onos",
                                   onos_password="rocks",
                                   onos_type="global")
        self.bandwidthProfile = BandwidthProfile(cbs=2000,
                                                 ebs=2700,
                                                 cir=2000000,
                                                 eir=2700000,
                                                 name="gold")
        self.userNetworkInterface = UserNetworkInterface(tenant="onf",
                                                         name="uni2",
                                                         latlng=[37.773972, -122.431297],
                                                         cpe_id="netconf:192.168.56.20:830/0")

        self.eline = ELine(name="testeline",
                           connect_point_1_id="netconf:10.6.0.160:830/0",
                           connect_point_2_id="netconf:10.6.0.161:830/0",
                           vlanids="100",
                           cord_site_name="onfGlobalONOS",
                           bwp="gold")

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

            desired_attrs = {"evcCfgId": "testeline",
                             "eir": 2700000,
                             "cir": 2000000,
                             "uniList": ["netconf:10.6.0.160:830/0", "netconf:10.6.0.161:830/0"],
                             "ebs": 2700,
                             "vlanId": 100,
                             "cbs": 2000,
                             "evcId": "testeline",
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
            self.assertEqual(url, "http://127.0.0.1:8182/carrierethernet/evc/testeline")

    def test_get_onos_global_addr(self):
        addr = self.syncstep.get_onos_global_addr(self.onosModel)
        self.assertEqual(addr, 'http://127.0.0.1:8182/carrierethernet/evc')

    def test_get_onos_global_auth(self):
        auth = self.syncstep.get_onos_global_auth(self.onosModel)
        self.assertEqual(auth.username, "onos")
        self.assertEqual(auth.password, "rocks")

if __name__ == '__main__':
    unittest.main()


