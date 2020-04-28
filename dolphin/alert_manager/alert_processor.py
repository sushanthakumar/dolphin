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

from oslo_log import log

from dolphin.drivers.manager import DriverManager
from dolphin.alert_manager.alert_model import AlertModel

LOG = log.getLogger(__name__)

class AlertProcessor(object):
    """Alert model translation and export functions"""

    def process_alert_info(self, alert_info, additional_info):
        """Fills alert model using driver manager interface."""

        # Get driver context from resource manager using source ip addr
        # TBD : if device has multiple interface (differnet ip)
        enterprise.oid -> driver type
        resource_manager.getDrvContext(enterprise.od)
        drv_context(manufacture=emc, serialno=abcd)
        drv_context = {}
        drv_alert_model = DriverManager().parse_alert(context, alert_info, additional_info[])
        alert_model = AlertModel.fill(drv_alert_model)
        self._export_alert_model(alert_model)

    def _export_alert_model(self, alert_model):
        """Exports the filled alert model to the export manager."""
