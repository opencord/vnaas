
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

from core.models import Tenant


class EnterpriseLocation(Tenant):

  KIND = "vnaas"

  class Meta:
      app_label = "vnaas"
      name = "vnaas"
      verbose_name = "Enterprise Location"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  cord_site_ip = CharField( help_text = "IP of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_port = IntegerField( help_text = "Port of the local site", max_length = 256, null = False, db_index = False, blank = False )
  cord_site_username = CharField( help_text = "Username of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_password = CharField( help_text = "Password of the local site", max_length = 64, null = False, db_index = False, blank = False )
  cord_site_type = CharField( default = "xos", choices = "(('onos', 'ONOS'), ('xos', 'XOS')", max_length = 64, blank = False, null = False, db_index = False )


  # Relations

  pass


class OnosModel(XOSBase):

  KIND = "vnaas"

  class Meta:
      app_label = "vnaas"
      name = "vnaas"
      verbose_name = "Open Network Operating System"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  onos_ip = CharField( help_text = "IP of the transport manager", max_length = 64, null = False, db_index = False, blank = False )
  onos_port = IntegerField( help_text = "Port of the transport manager", max_length = 256, null = False, db_index = False, blank = False )
  onos_username = CharField( help_text = "Username of the transport manager", max_length = 64, null = False, db_index = False, blank = False )
  onos_password = CharField( help_text = "Password of the transport manager", max_length = 64, null = False, db_index = False, blank = False )
  onos_type = CharField( default = "local", choices = "(('local', 'Local'), ('global', 'Global')", max_length = 64, blank = False, null = False, db_index = False )


  # Relations


  pass


class UserNetworkInterface(XOSBase):

  KIND = "vnaas"

  class Meta:
      app_label = "vnaas"
      name = "vnaas"
      verbose_name = "User Network Interface"

  # Primitive Fields (Not Relations)
  tenant = CharField( help_text = "Tenant name", max_length = 256, null = False, db_index = False, blank = False )
  cpe_id = CharField( blank = False, max_length = 1024, null = False, db_index = False )
  latlng = CharField( help_text = "Location, i.e. [37.773972, -122.431297]", max_length = 256, null = False, db_index = False, blank = False )
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )


  # Relations


  def __unicode__(self):  return u'%s' % (self.name)

  def save(self, *args, **kwargs):

      if self.latlng:
          try:
              latlng_value = getattr(self, 'latlng').strip()
              if (latlng_value.startswith('[') and latlng_value.endswith(']') and latlng_value.index(',') > 0):
                  lat = latlng_value[1: latlng_value.index(',')].strip()
                  lng = latlng_value[latlng_value.index(',') + 1: len(latlng_value) - 1].strip()

                  # If lat and lng are not floats, the code below should result in an error.
                  lat_validation = float(lat)
                  lng_validation = float(lng)
              else:
                  raise ValueError("The lat/lng value is not formatted correctly.")
          except:
              raise ValueError("The lat/lng value is not formatted correctly.")

      super(UserNetworkInterface, self).save(*args, **kwargs)
  pass




class BandwidthProfile(XOSBase):

  KIND = "vnaas"

  class Meta:
      app_label = "vnaas"
      name = "vnaas"
      verbose_name = "Bandwidth Profile"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  cbs = IntegerField( help_text = "Committed burst size", null = False, blank = False, db_index = False )
  ebs = IntegerField( help_text = "Expected burst size", null = False, blank = False, db_index = False )
  cir = IntegerField( help_text = "Committed information rate", null = False, blank = False, db_index = False )
  eir = IntegerField( help_text = "Expected information rate", null = False, blank = False, db_index = False )


  # Relations


  def __unicode__(self):  return u'%s' % (self.name)
  pass



class ELine(XOSBase):

  KIND = "vnaas"

  class Meta:
      app_label = "vnaas"
      name = "vnaas"
      verbose_name = "Ethernet Virtual Private Line"

  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 256, null = False, db_index = False )
  connect_point_1_id = CharField( blank = False, max_length = 256, null = False, db_index = False )
  connect_point_2_id = CharField( blank = False, max_length = 64, null = False, db_index = False )
  vlanids = TextField( help_text = "comma separated list of vlanIds", null = False, blank = False, db_index = False )
  cord_site_username = CharField( blank = False, max_length = 64, null = False, db_index = False )
  bwp = CharField( help_text = "bandwidth profile name", max_length = 256, null = False, db_index = False, blank = False )


  # Relations


  def __unicode__(self):  return u'%s' % (self.name)
  pass

