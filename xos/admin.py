
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


# admin.py - vNaaSworkService Django Admin

from core.admin import ReadOnlyAwareAdmin
from core.admin import XOSBaseAdmin
from django.contrib import admin
from django import forms


class XOSvNaaSBandwithProfileAdmin(XOSBaseAdmin):
    verbose_name = "Bandwidth Profile"
    list_display = ('cbs','ebs','cir','eir','name')

    fields = ('cbs', 'ebs', 'cir', 'eir', 'name')

class XOSvNaaSUNIAdmin(XOSBaseAdmin):
    verbose_name = "User Network Interface"
    list_display = ('tenant', 'vlanIds', 'cpe_id', 'latlng', 'name')
    fields = ('tenant','vlanIds', 'cpe_id', 'latlng', 'name')

class XOSvNaaSEnterpriseLocationAdmin(XOSBaseAdmin):
    verbose_name = "Enterprise Location"
    list_display = ('name', 'cord_site_ip', 'cord_site_port', 'cord_site_username', 'cord_site_password', 'cord_site_type')
    fields = ('name', 'cord_site_ip', 'cord_site_port', 'cord_site_username', 'cord_site_password', 'cord_site_type')

class XOSvNaaSOnosModelAdmin(XOSBaseAdmin):
    verbose_name = "Open Network Operating System"
    list_display = ('name', 'onos_ip', 'onos_port', 'onos_username', 'onos_password', 'onos_type')
    fields = ('name', 'onos_ip', 'onos_port', 'onos_username', 'onos_password', 'onos_type')

class XOSvNaaSELineAdmin(XOSBaseAdmin):
    verbose_name = "Ethernet Virtual Private Line"
    list_display = ('name', 'connect_point_1_id', 'connect_point_2_id', 'vlanids', 'cord_site_name', 'bwp')
    fields = ('name', 'connect_point_1_id', 'connect_point_2_id', 'vlanids', 'cord_site_name', 'bwp')

admin.site.register(XOSvNaaSBandwithProfile, XOSvNaaSBandwithProfileAdmin)
admin.site.register(XOSvNaaSUNI, XOSvNaaSUNIAdmin)
admin.site.register(XOSvNaaSEnterpriseLocation, XOSvNaaSEnterpriseLocationAdmin)
admin.site.register(XOSvNaaSOnosModel, XOSvNaaSOnosModelAdmin)
admin.site.register(XOSvNaaSELine, XOSvNaaSELineAdmin)