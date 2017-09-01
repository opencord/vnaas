
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


from xosresource import XOSResource
from service import XOSService
from services.vnaas.models import *

class XOSvNaaSUNI(XOSResource):
    provides = "tosca.nodes.UserNetworkInterface"
    xos_model = UserNetworkInterface
    copyin_props = ['tenant','vlanIds', 'cpe_id', 'latlng', 'name']

class XOSvNaaSEnterpriseLocation(XOSResource):
    provides = "tosca.nodes.EnterpriseLocation"
    xos_model = EnterpriseLocation
    copyin_props = ['name', 'cord_site_ip', 'cord_site_port', 'cord_site_username', 'cord_site_password', 'cord_site_type']

class XOSvNaaSOnosModel(XOSResource):
    provides = "tosca.nodes.OnosModel"
    xos_model = OnosModel
    copyin_props = ['name', 'onos_ip', 'onos_port', 'onos_username', 'onos_password', 'onos_type']

class XOSvNaaSBandwithProfile(XOSResource):
    provides = "tosca.nodes.BandwidthProfile"
    xos_model = BandwidthProfile
    copyin_props = ['cbs', 'ebs', 'cir', 'eir', 'name']

class XOSvNaaSELine(XOSResource):
    provides = "tosca.nodes.ELine"
    xos_model = ELine
    copyin_props = ['name', 'connect_point_1_id', 'connect_point_2_id', 'vlanids', 'cord_site_name', 'bwp']