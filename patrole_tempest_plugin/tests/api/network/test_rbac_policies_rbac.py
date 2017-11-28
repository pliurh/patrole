# All Rights Reserved.
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
#

import netaddr

from tempest.common import utils
from tempest.common.utils import net_utils
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_exceptions
from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.network import rbac_base as base

CONF = config.CONF


class RbacPoliciesRbacTest(base.BaseNetworkRbacTest):

    @classmethod
    def resource_setup(cls):
        super(RbacPoliciesRbacTest, cls).resource_setup()
        cls.network = cls.create_network()

    def _create_rbac_policy(self,
                            target_tenant=None,
                            action=None,
                            type=None,
                            uuid=None):
        pass

    @rbac_rule_validation.action(service="neutron",
                                 rule="create_rbac_policy")
    @decorators.idempotent_id('95b9baab-1ece-4e2b-89c8-8d671d974e54')
    def test_create_rbac_policy(self):

        """Create RBAC policy Test

        RBAC test for the neutron create_rbac_policy
        """
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self._create_rbac_policy("network", )

    @rbac_rule_validation.action(service="neutron",
                                 rule="create_rbac_policy:target_tenant")
    @decorators.idempotent_id('95b9baab-1ece-4e2b-89c8-8d671d974e54')
    def test_create_rbac_target_tenant_policy(self):

        """Create RBAC policy Test

        RBAC test for the neutron create_rbac_policy:target_tenant
        """
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)

    @rbac_rule_validation.action(service="neutron",
                                 rule="update_rbac_policy")
    @decorators.idempotent_id('95b9baab-1ece-4e2b-89c8-8d671d974e54')
    def test_update_rbac_policy(self):
        """Update RBAC policy Test

        RBAC test for the neutron update_rbac_policy
        """
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)

    @rbac_rule_validation.action(service="neutron",
                                 rule="update_rbac_policy:target_tenant")
    @decorators.idempotent_id('95b9baab-1ece-4e2b-89c8-8d671d974e54')
    def test_update_target_tenant_rbac_policy(self):
        """Update RBAC policy Test

        RBAC test for the neutron update_rbac_policy:target_tenant
        """
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)

    @rbac_rule_validation.action(service="neutron",
                                 rule="get_rbac_policy")
    @decorators.idempotent_id('95b9baab-1ece-4e2b-89c8-8d671d974e54')
    def test_get_rbac_policy(self):
        """Get RBAC policy Test

        RBAC test for the neutron update_rbac_policy
        """
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)

    @rbac_rule_validation.action(service="neutron",
                                 rule="delete_rbac_policy")
    @decorators.idempotent_id('95b9baab-1ece-4e2b-89c8-8d671d974e54')
    def test_delete_rbac_policy(self):
        """Delete RBAC policy Test

        RBAC test for the neutron update_rbac_policy
        """
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)