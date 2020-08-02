# Copyright 2020 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_log import log

from delfin import db
from delfin import exception
from delfin.api import validation
from delfin.api.common import wsgi
from delfin.drivers import api as driver_manager
from delfin.api.schemas import alerts as schema_alerts

LOG = log.getLogger(__name__)


class AlertsController(wsgi.Controller):
    def __init__(self):
        super().__init__()
        self.driver_manager = driver_manager.API()

    @wsgi.response(200)
    @validation.schema(schema_alerts.delete)
    def delete(self, req, id, body):
        ctx = req.environ['delfin.context']

        try:
            _ = db.storage_get(ctx, id)
        except exception.StorageNotFound:
            raise exception.StorageNotFound(id)
        self.driver_manager.clear_alert(ctx, id, body['sequence_number'])


def create_resource():
    return wsgi.Resource(AlertsController())
