
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


tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vnaas.m4 > vnaas.yaml"

# include macros
include(macros.m4)

node_types:

    tosca.nodes.BandwidthProfile:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The E-CORD bandwidth profile.
        capabilities:
        properties:
            no-delete:
                type: boolean
                default: false
                description: Do not allow Tosca to delete this object
            no-create:
                type: boolean
                default: false
                description: Do not allow Tosca to create this object
            no-update:
                type: boolean
                default: false
                description: Do not allow Tosca to update this object
            replaces:
                type: string
                required: false
                descrption: Replaces/renames this object
            cbs:
                type: integer
                required: false
            ebs:
                type: integer
                required: false
            cir:
                type: integer
                required: false
            eir:
                type: integer
                required: false
            name:
                type: string
                required: true

    tosca.nodes.UserNetworkInterface:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The ecord user netowrk interface
        capabilities:
        properties:
            no-delete:
                type: boolean
                default: false
                description: Do not allow Tosca to delete this object
            no-create:
                type: boolean
                default: false
                description: Do not allow Tosca to create this object
            no-update:
                type: boolean
                default: false
                description: Do not allow Tosca to update this object
            replaces:
                type: string
                required: false
                descrption: Replaces/renames this object
            cpe_id:
                type: string
                required: false
            tenant:
                type: string
                required: true
            name:
                type: string
                required: true
            latlng:
                type: string
                required: false

    tosca.nodes.OnosModel:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The ecord ONOS model
        capabilities:
        properties:
            no-delete:
                type: boolean
                default: false
                description: Do not allow Tosca to delete this object
            no-create:
                type: boolean
                default: false
                description: Do not allow Tosca to create this object
            no-update:
                type: boolean
                default: false
                description: Do not allow Tosca to update this object
            replaces:
                type: string
                required: false
                descrption: Replaces/renames this object
            name:
                type: string
                required: false
            onos_ip:
                type: string
                required: false
            onos_port:
                type: integer
                required: false
            onos_username:
                type: string
                required: false
            onos_password:
                type: string
                required: false
            onos_type:
                type: string
                required: false

    tosca.nodes.EnterpriseLocation:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The ecord enterprise location
        capabilities:
        properties:
            no-delete:
                type: boolean
                default: false
                description: Do not allow Tosca to delete this object
            no-create:
                type: boolean
                default: false
                description: Do not allow Tosca to create this object
            no-update:
                type: boolean
                default: false
                description: Do not allow Tosca to update this object
            replaces:
                type: string
                required: false
                descrption: Replaces/renames this object
            name:
                type: string
                required: false
            cord_site_ip:
                type: string
                required: false
            cord_site_port:
                type: integer
                required: false
            cord_site_username:
                type: string
                required: false
            cord_site_password:
                type: string
                required: false
            cord_site_type:
                type: string
                required: false

    tosca.nodes.ELine:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The ecord Ethernet Virtual Private Line
        capabilities:
        properties:
            no-delete:
                type: boolean
                default: false
                description: Do not allow Tosca to delete this object
            no-create:
                type: boolean
                default: false
                description: Do not allow Tosca to create this object
            no-update:
                type: boolean
                default: false
                description: Do not allow Tosca to update this object
            replaces:
                type: string
                required: false
                descrption: Replaces/renames this object
            name:
                type: string
                required: false
            connect_point_1_id:
                type: string
                required: false
            connect_point_2_id:
                type: string
                required: false
            vlanids:
                type: string
                required: false
            cord_site_name:
                type: string
                required: false
            bwp:
                type: string
                required: false