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

from tempest.api.network import base as network_base
from tempest import config

from patrole_tempest_plugin import rbac_utils

CONF = config.CONF


class BaseNetworkRbacTest(network_base.BaseNetworkTest):

    @classmethod
    def skip_checks(cls):
        super(BaseNetworkRbacTest, cls).skip_checks()
        if not CONF.patrole.enable_rbac:
            raise cls.skipException(
                "%s skipped as RBAC testing not enabled" % cls.__name__)

    @classmethod
    def setup_clients(cls):
        super(BaseNetworkRbacTest, cls).setup_clients()
        cls.rbac_utils = rbac_utils.RbacUtils(cls)
