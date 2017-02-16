# Copyright 2017 AT&T Corporation.
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

from tempest.common.utils import data_utils
from tempest import config
from tempest.lib.common.utils import test_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.rbac_utils import rbac_utils
from patrole_tempest_plugin.tests.api.identity.v3 import rbac_base

CONF = config.CONF


class IdentityGroupsV3AdminRbacTest(rbac_base.BaseIdentityV3RbacAdminTest):

    def tearDown(self):
        """Reverts user back to admin for cleanup."""
        rbac_utils.switch_role(self, switchToRbacRole=False)
        super(IdentityGroupsV3AdminRbacTest, self).tearDown()

    def _create_group(self):
        """Creates a group for test."""
        name = data_utils.rand_name('Group')
        group = self.groups_client \
                    .create_group(name=name)['group']

        self.addCleanup(test_utils.call_and_ignore_notfound_exc,
                        self.groups_client.delete_group, group['id'])
        return group

    def _add_user_to_group(self, group_id):
        """Creates a user and adds to a group for test."""
        user_name = data_utils.rand_name('User')
        user = self._create_test_user(name=user_name, password=None)

        self.groups_client.add_group_user(group_id, user['id'])

        return user['id']

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:create_group")
    @decorators.idempotent_id('88377f51-9074-4d64-a22f-f8931d048c9a')
    def test_create_group(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        self._create_group()

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:update_group")
    @decorators.idempotent_id('790fb7be-a657-4a64-9b83-c43425cf180b')
    def test_update_group(self):
        group = self._create_group()
        # Update Group
        new_name = data_utils.rand_name('UpdateGroup')

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.update_group(group['id'],
                                        name=new_name)

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:delete_group")
    @decorators.idempotent_id('646b52da-2a5f-486a-afb0-51fdc86a6c12')
    def test_delete_group(self):
        group = self._create_group()

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.delete_group(group['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:get_group")
    @decorators.idempotent_id('d530f0ad-42b9-429b-ad05-e53ac95a040e')
    def test_show_group(self):
        group = self._create_group()

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.show_group(group['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:list_groups")
    @decorators.idempotent_id('c4d0f76b-735f-4fd0-868b-0006bc420ff4')
    def test_list_groups(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.list_groups()

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:add_user_to_group")
    @decorators.idempotent_id('fdd49b74-3ed3-4736-9f0e-9027a32017ac')
    def test_add_user_group(self):
        group = self._create_group()

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self._add_user_to_group(group['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:remove_user_from_group")
    @decorators.idempotent_id('8a60d11c-7d2b-47e5-a0f3-9ea900ca66fe')
    def test_remove_user_group(self):
        group = self._create_group()
        user_id = self._add_user_to_group(group['id'])

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.delete_group_user(group['id'], user_id)

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:list_users_in_group")
    @decorators.idempotent_id('b3e394a7-079e-4a0d-a4ff-9b266293d1ee')
    def test_list_user_group(self):
        group = self._create_group()

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.list_group_users(group['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rule="identity:check_user_in_group")
    @decorators.idempotent_id('d3603241-fd87-4a2d-94f9-f32469d1aaba')
    def test_check_user_group(self):
        group = self._create_group()
        user_id = self._add_user_to_group(group['id'])

        rbac_utils.switch_role(self, switchToRbacRole=True)
        self.groups_client.check_group_user_existence(group['id'], user_id)