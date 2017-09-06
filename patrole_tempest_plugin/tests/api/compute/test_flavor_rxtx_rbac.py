#    Copyright 2017 AT&T Corporation.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

from tempest.lib import decorators
from tempest import test

from patrole_tempest_plugin import rbac_exceptions
from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.compute import rbac_base

CONF = cfg.CONF


class FlavorRxtxRbacTest(rbac_base.BaseV2ComputeRbacTest):

    @classmethod
    def skip_checks(cls):
        super(FlavorRxtxRbacTest, cls).skip_checks()
        if not test.is_extension_enabled('os-flavor-rxtx', 'compute'):
            msg = "os-flavor-rxtx extension not enabled."
            raise cls.skipException(msg)

    @decorators.idempotent_id('5e1fd9f0-9a08-485a-ad9c-0fc66e4d64b7')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-flavor-rxtx")
    def test_list_flavors_details_rxtx(self):
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        # Enforces os_compute_api:os-flavor-rxtx
        result = self.flavors_client.list_flavors(detail=True)['flavors']
        if 'rxtx_factor' not in result[0]:
            raise rbac_exceptions.RbacMalformedResponse(
                attribute='rxtx_factor')

    @decorators.idempotent_id('70c55a07-c843-4627-a29d-ba78673c1e63')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-flavor-rxtx")
    def test_get_flavor_rxtx(self):
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        # Enforces os_compute_api:os-flavor-rxtx
        result =\
            self.flavors_client.show_flavor(CONF.compute.flavor_ref)['flavor']
        if 'rxtx_factor' not in result:
            raise rbac_exceptions.RbacMalformedResponse(
                attribute='rxtx_factor')
