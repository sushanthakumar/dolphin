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

from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher

from delfin import exception
from delfin.alert_manager import alert_processor


def fake_storage_info():
    return {
        'id': 'abcd-1234-56789',
        'name': 'storage1',
        'vendor': 'fake manufacturer',
        'model': 'fake product',
        'serial_number': 'serial-1234',
    }


def fake_alert_model():
    return {'storage_id': 'abcd-1234-56789',
            'storage_name': 'storage1',
            'manufacturer': 'fake manufacturer',
            'product_name': 'fake product',
            'serial_number': 'serial-1234',
            'alert_id': '1050',
            'alert_name': 'SAMPLE_ALERT_NAME',
            'severity': alert_processor.Severity.WARNING,
            'category': alert_processor.Category.NOT_SPECIFIED,
            'type': 'topology',
            'sequence_number': 79,
            'detailed_info': 'Diagnostic event trace triggered.',
            'recovery_advice': 'NA',
            'resource_type': alert_processor.ResourceType.STORAGE,
            'location': 'Array id=000192601409,Component type=location1 '
                        'Group,Component name=comp1,Event source=symmetrix',
            }


def fake_v3_alert_source():
    return {'storage_id': 'abcd-1234-5678',
            'version': 'snmpv3',
            'engine_id': '800000d30300000e112245',
            'username': 'test1',
            'auth_key': 'YWJjZDEyMzQ1Njc=',
            'auth_protocol': 'md5',
            'privacy_key': 'YWJjZDEyMzQ1Njc=',
            'privacy_protocol': 'des'
            }


def fake_v3_alert_source_list_with_one():
    return [
        {'storage_id': 'abcd-1234-5678',
         'version': 'snmpv3',
         'engine_id': '800000d30300000e112245',
         'username': 'test1',
         'auth_key': 'YWJjZDEyMzQ1Njc=',
         'auth_protocol': 'md5',
         'privacy_key': 'YWJjZDEyMzQ1Njc=',
         'privacy_protocol': 'des'
         }
    ]


def null_alert_source_list():
    return []


def fake_v3_alert_source_list():
    return [
        {'storage_id': 'abcd-1234-5678',
         'version': 'snmpv3',
         'engine_id': '800000d30300000e112245',
         'username': 'test1',
         'auth_key': 'YWJjZDEyMzQ1Njc=',
         'auth_protocol': 'md5',
         'privacy_key': 'YWJjZDEyMzQ1Njc=',
         'privacy_protocol': 'des'
         },
        {'storage_id': 'abcd-1234-5677',
         'version': 'snmpv3',
         'engine_id': '800000d30300000e112246',
         'username': 'test2',
         'auth_key': 'YWJjZDEyMzQ1Njc=',
         'auth_protocol': 'md5',
         'privacy_key': 'YWJjZDEyMzQ1Njc=',
         'privacy_protocol': 'des'
         }
    ]


def parse_alert_exception():
    raise exception.InvalidResults("parse alert failed.")


def load_config_exception(para):
    raise exception.InvalidResults("load config failed.")


def mock_add_transport(snmpEngine, transportDomain, transport):
    snmpEngine.transportDispatcher = AsyncoreDispatcher()
