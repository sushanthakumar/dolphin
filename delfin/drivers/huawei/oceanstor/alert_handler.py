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

from delfin import exception
from delfin.alert_manager import alert_processor
from delfin.i18n import _

LOG = log.getLogger(__name__)


class AlertHandler(object):
    """Alert handling functions for huawei oceanstor driver"""
    default_me_category = 'storage-subsystem'

    SEVERITY_MAP = {"Critical alarm": alert_processor.Severity.CRITICAL,
                    "Major alarm": alert_processor.Severity.MAJOR,
                    "Minor alarm": alert_processor.Severity.MINOR,
                    "Warning alarm": alert_processor.Severity.WARNING}

    CATEGORY_MAP = {"Fault alarm": alert_processor.Category.FAULT,
                    "Recovery alarm": alert_processor.Category.RECOVERY,
                    "Event alarm": alert_processor.Category.EVENT}

    # Attributes expected in alert info to proceed with model filling
    expected_alert_attributes = ('emcAsyncEventCode', 'connUnitEventSeverity',
                                 'connUnitEventType', 'connUnitEventDescr',
                                 'connUnitType', 'emcAsyncEventComponentType',
                                 'emcAsyncEventComponentName',
                                 'emcAsyncEventSource')

    def __init__(self):
        pass

    """
    Alert model contains below fields
    category : Type of the reported notification
    occur_time : Time of occurrence of alert. When trap does not contain it,
                 it will be filled with receive time
    match_key : This info uniquely identifies the fault point. Several infos
                such as source system id, location, alarm id together can be
                used to construct this
    me_dn : Unique id at resource module (management system) side. me stands
            for management element here
    me_name : Unique name at resource module (management system) side
    native_me_dn : Unique id of the device at source system that reports the
                   alarm
    location : Alarm location information. It helps to locate the lowest unit
               where fault is originated(Name-value pairs)
               ex: Location = subtrack, No = 1, Slot No = 5.
                   shelf Id = 1, board type = ADSL
    event_type : Basic classification of the alarm. Probable values such as
                 status, configuration, topology ....
    alarm_id : Identification of alarm
    alarm_name : Name of the alarm, might need translation from alarm id
    severity : Severity of alarm. Helps admin to decide on action to be taken
               Probable values: Critical, Major, Minor, Warning, Info
    device_alert_sn : Sequence number of alert generated. This will be helpful
                      during alert clearing process
    manufacturer : Vendor of the device
    Product_name : Name of the product
    probable_cause : Probable reason for alert generation
    clear_type : Alarm clearance type such as manual, automatic, reset clear
    me_category : Resource category of the device generating the alarm
                  Probable value: Network,Server,Storage..
    """

    """
     Alert Model	Description
     *****Filled from delfin resource info***********************
     storage_id	Id of the storage system on behalf of which alert is generated
     storage_name	Name of the storage system on behalf of which alert is 
                     generated
     manufacturer	Vendor of the device
     product_name	Product or the model name
     serial_number	Serial number of the alert generating source
     ****************************************************

     *****Filled from driver side ***********************
     source_id	Identification of alerting device at source side such as 
                  node id, array id etc
     alert_id	Unique identification for a given alert type
     alert_name	Unique name for a given alert type
     severity	Severity of the alert
     category	Category of alert generated
     type	Type of the alert generated
     sequence_number	Sequence number for the alert, uniquely identifies a 
                               given alert instance used for clearing the alert
     occur_time	Time at which alert is generated from device
     detailed_info	Possible cause description or other details about the alert
     recovery_advice	Some suggestion for handling the given alert
     resource_type	Resource type of device/source generating alert
     location	Detailed info about the tracing the alerting device uch as 
                 slot, rack, component, parts etc
     clear_type	Indicates the way to clear this alert
     *****************************************************
     """

    def parse_alert(self, context, alert):
        """Parse alert data got from alert manager and fill the alert model."""

        try:
            alert_model = {}
            # These information are sourced from device registration info
            alert_model['source_id'] = alert['hwIsmReportingAlarmNodeCode']
            alert_model['alert_id'] = alert['hwIsmReportingAlarmAlarmID']
            alert_model['alert_name'] = alert['hwIsmReportingAlarmFaultTitle']
            alert_model['severity'] = self.SEVERITY_MAP.get(
                alert['hwIsmReportingAlarmFaultLevel'],
                alert_processor.Severity.NOT_SPECIFIED)
            alert_model['category'] = self.CATEGORY_MAP.get(
                alert['hwIsmReportingAlarmFaultCategory'],
                alert_processor.Category.NOT_SPECIFIED)
            alert_model['type'] = alert['hwIsmReportingAlarmFaultType']
            alert_model['sequence_number'] \
                = alert['hwIsmReportingAlarmSerialNo']
            alert_model['occur_time'] = alert['hwIsmReportingAlarmFaultTime']
            alert_model['detailed_info'] \
                = alert['hwIsmReportingAlarmAdditionInfo']
            alert_model['recovery_advice'] \
                = alert['hwIsmReportingAlarmRestoreAdvice']
            alert_model['resource_type'] = alert_processor.ResourceType.STORAGE
            alert_model['location'] = alert['hwIsmReportingAlarmLocationInfo']

            return alert_model
        except Exception as e:
            LOG.error(e)
            msg = (_("Failed to build alert model as some attributes missing "
                     "in alert message."))
            raise exception.InvalidResults(msg)

    def add_trap_config(self, context, storage_id, trap_config):
        """Config the trap receiver in storage system."""
        # Currently not implemented
        pass

    def remove_trap_config(self, context, storage_id, trap_config):
        """Remove trap receiver configuration from storage system."""
        # Currently not implemented
        pass

    def clear_alert(self, context, storage_id, alert):
        # Currently not implemented
        """Clear alert from storage system."""
        pass
