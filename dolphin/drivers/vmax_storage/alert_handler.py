# Copyright 2020 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json

from oslo_log import log

LOG = log.getLogger(__name__)

class AlertHandler(object):
    """Alert handling functions for vmax driver"""

    def __init__(self):

    def add_trap_config(self, context, storage_id, trap_config):
        """Config the trap receiver in storage system."""
        pass

    def remove_trap_config(self, context, storage_id, trap_config):
        """Remove trap receiver configuration from storage system."""
        pass

    def parse_alert(self, context, alert_info, additional_info):
        """Parse alert data got from snmp trap server."""
        input = json (10 fields)
        output = filled json (alert model = 20 fileds)

    def clear_alert(self, context, storage_id, alert):
        """Clear alert from storage system."""
        pass