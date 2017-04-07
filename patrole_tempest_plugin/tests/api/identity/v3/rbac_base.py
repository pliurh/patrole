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

from tempest.api.identity import base
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib.common.utils import test_utils

from patrole_tempest_plugin.rbac_utils import rbac_utils

CONF = config.CONF


class BaseIdentityV3RbacAdminTest(base.BaseIdentityV3AdminTest):

    credentials = ['admin', 'primary']

    @classmethod
    def skip_checks(cls):
        super(BaseIdentityV3RbacAdminTest, cls).skip_checks()
        if not CONF.rbac.enable_rbac:
            raise cls.skipException(
                "%s skipped as RBAC Flag not enabled" % cls.__name__)

    @classmethod
    def setup_clients(cls):
        super(BaseIdentityV3RbacAdminTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider

        cls.rbac_utils = rbac_utils()
        cls.rbac_utils.switch_role(cls, toggle_rbac_role=False)

        cls.creds_client = cls.os.credentials_client
        cls.consumers_client = cls.os.oauth_consumers_client
        cls.domains_client = cls.os.domains_client
        cls.endpoints_client = cls.os.endpoints_v3_client
        cls.groups_client = cls.os.groups_client
        cls.projects_client = cls.os.projects_client
        cls.policies_client = cls.os.policies_client
        cls.regions_client = cls.os.regions_client
        cls.role_assignments_client = cls.os.role_assignments_client
        cls.roles_client = cls.os.roles_v3_client
        cls.services_client = cls.os.identity_services_v3_client
        cls.users_client = cls.os.users_v3_client

    @classmethod
    def resource_setup(cls):
        super(BaseIdentityV3RbacAdminTest, cls).resource_setup()
        cls.credentials = []
        cls.domains = []
        cls.endpoints = []
        cls.groups = []
        cls.policies = []
        cls.projects = []
        cls.regions = []
        cls.roles = []
        cls.services = []
        cls.users = []

    @classmethod
    def resource_cleanup(cls):
        for credential in cls.credentials:
            test_utils.call_and_ignore_notfound_exc(
                cls.creds_client.delete_credential, credential['id'])

        # Delete each domain at the end of the test, but each domain must be
        # disabled first.
        for domain in cls.domains:
            test_utils.call_and_ignore_notfound_exc(
                cls.domains_client.update_domain, domain['id'], enabled=False)
            test_utils.call_and_ignore_notfound_exc(
                cls.domains_client.delete_domain, domain['id'])

        for endpoint in cls.endpoints:
            test_utils.call_and_ignore_notfound_exc(
                cls.endpoints_client.delete_endpoint, endpoint['id'])

        for group in cls.groups:
            test_utils.call_and_ignore_notfound_exc(
                cls.groups_client.delete_group, group['id'])

        for policy in cls.policies:
            test_utils.call_and_ignore_notfound_exc(
                cls.policies_client.delete_policy, policy['id'])

        for project in cls.projects:
            test_utils.call_and_ignore_notfound_exc(
                cls.projects_client.delete_project, project['id'])

        for region in cls.regions:
            test_utils.call_and_ignore_notfound_exc(
                cls.regions_client.delete_region, region['id'])

        for role in cls.roles:
            test_utils.call_and_ignore_notfound_exc(
                cls.roles_client.delete_role, role['id'])

        for service in cls.services:
            test_utils.call_and_ignore_notfound_exc(
                cls.services_client.delete_service, service['id'])

        for user in cls.users:
            test_utils.call_and_ignore_notfound_exc(
                cls.users_client.delete_user, user['id'])

        super(BaseIdentityV3RbacAdminTest, cls).resource_cleanup()

    @classmethod
    def setup_test_credential(cls, user=None):
        """Creates a credential for test."""
        keys = [data_utils.rand_uuid_hex(),
                data_utils.rand_uuid_hex()]
        blob = '{"access": "%s", "secret": "%s"}' % (keys[0], keys[1])

        credential = cls.creds_client.create_credential(
            user_id=user['id'],
            project_id=user['project_id'],
            blob=blob,
            type='ec2')['credential']
        cls.credentials.append(credential)

        return credential

    @classmethod
    def setup_test_domain(cls):
        """Set up a test domain."""
        domain = cls.domains_client.create_domain(
            name=data_utils.rand_name('test_domain'),
            description=data_utils.rand_name('desc'))['domain']
        cls.domains.append(domain)

        return domain

    @classmethod
    def setup_test_endpoint(cls, service=None):
        """Creates a service and an endpoint for test."""
        interface = 'public'
        url = data_utils.rand_url()
        # Endpoint creation requires a service
        if service is None:
            service = cls.setup_test_service()

        endpoint = cls.endpoints_client.create_endpoint(
            service_id=service['id'],
            interface=interface,
            url=url)['endpoint']
        cls.endpoints.append(endpoint)

        return endpoint

    @classmethod
    def setup_test_group(cls):
        """Creates a group for test."""
        name = data_utils.rand_name('test_group')
        group = cls.groups_client.create_group(name=name)['group']
        cls.groups.append(group)

        return group

    @classmethod
    def setup_test_policy(cls):
        """Creates a policy for test."""
        blob = data_utils.rand_name('test_blob')
        policy_type = data_utils.rand_name('policy_type')

        policy = cls.policies_client.create_policy(
            blob=blob,
            policy=policy_type,
            type="application/json")['policy']
        cls.policies.append(policy)

        return policy

    @classmethod
    def setup_test_project(cls):
        """Set up a test project."""
        project = cls.projects_client.create_project(
            name=data_utils.rand_name('test_project'),
            description=data_utils.rand_name('desc'))['project']
        cls.projects.append(project)

        return project

    @classmethod
    def setup_test_region(cls):
        """Creates a region for test."""
        description = data_utils.rand_name('test_region_desc')

        region = cls.regions_client.create_region(
            description=description)['region']
        cls.regions.append(region)

        return region

    @classmethod
    def setup_test_role(cls):
        """Set up a test role."""
        name = data_utils.rand_name('test_role')
        role = cls.roles_client.create_role(name=name)['role']
        cls.roles.append(role)

        return role

    @classmethod
    def setup_test_service(cls):
        """Setup a test service."""
        name = data_utils.rand_name('service')
        serv_type = data_utils.rand_name('type')
        desc = data_utils.rand_name('description')

        service = cls.services_client.create_service(
            name=name,
            type=serv_type,
            description=desc)['service']
        cls.services.append(service)

        return service

    @classmethod
    def setup_test_user(cls, password=None, **kwargs):
        """Set up a test user."""
        username = data_utils.rand_name('test_user')
        email = username + '@testmail.tm'

        user = cls.users_client.create_user(
            name=username,
            email=email,
            password=password,
            **kwargs)['user']
        cls.users.append(user)

        return user
