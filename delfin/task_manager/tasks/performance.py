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

import copy
from datetime import datetime

from oslo_log import log
from oslo_utils import uuidutils

from delfin import context
from delfin import db
from delfin import exception
from delfin.common import constants, config
from delfin.drivers import api as driverapi
from delfin.exporter import base_exporter
from delfin.i18n import _
from delfin.task_manager.tasks import performance

LOG = log.getLogger(__name__)


class PeriodicScheduler(object):

    def __init__(self):
        self.performance_collector = performance.PerformanceCollectionTask()
        pass

    def initiate(self):
        """
        """
        ctxt = context.get_admin_context()
        try:
            schedule = config.Scheduler.getInstance()
            periodic_scheduler_job_id = uuidutils.generate_uuid()
            schedule.add_job(
                self.schedule_collection, 'interval', args=[ctxt],
                seconds=constants.Task.DEFAULT_INTERVAL,
                next_run_time=datetime.now(),
                id=periodic_scheduler_job_id)
            LOG.info(
                "Periodic schedular for performance collection started")
        except Exception as e:
            LOG.error("Failed to trigger periodic scheduler for performance "
                      "collection")
            raise exception.InvalidContentType(e)
        else:
            # start the scheduler
            schedule.start()

    def schedule_collection(self, ctx):
        """
        :return:
        """
        try:
            # create the object of periodic scheduler
            schedule = config.Scheduler.getInstance()
            task_templates = db.task_template_get_all(ctx)

            LOG.info(
                "************************************************************************")

            if not len(task_templates):
                LOG.info("No task templates found for performance collection")
                LOG.info(
                    "************************************************************************")
                return

            LOG.info("Schedule performance collection triggered: total "
                     "templates:%s" % len(task_templates))
            LOG.info(
                "************************************************************************")
            for task_template in task_templates:
                # Get current time in epoch format
                current_time = int(datetime.utcnow().timestamp()) * 1000
                task_template['last_run_time'] = current_time
                db.task_template_update(ctx, task_template['id'],
                                        task_template)

                LOG.info("Processing task template : %s" % task_template['id'])

                task_instance = {}
                task_instance['storage_id'] = task_template['storage_id']
                task_instance['task_template_id'] = task_template['id']
                interval = task_template['interval']
                task_instance['method'] = task_template['method']
                task_instance['interval'] = interval
                task_instance['args'] = task_template['args']
                task_instance['retry_count'] \
                    = constants.Task.MAX_TASK_RETRY_COUNT

                LOG.info("Adding task instance : %s" % task_template)

                # Add task instance to db
                task_instance = db.task_instance_create(context, task_instance)

                # Create collection task
                task_instance_id = task_instance['id']
                schedule.add_job(
                    self.performance_collector.collect, 'interval',
                    args=[ctx, task_instance_id],
                    seconds=interval, next_run_time=datetime.now(),
                    id=task_instance_id)

                task_instance = dict(task_instance)
                LOG.info("************Task instance status*********")
                for k in task_instance:
                    LOG.info("%s : %s" % (k, task_instance[k]))
                LOG.info("************************************************")

        except Exception as e:
            LOG.error("Failed to trigger performance collection tasks")
            raise exception.InvalidContentType(e)
        else:
            # start the scheduler
            LOG.info("Schedule collection completed")


class PerformanceCollectionTask(object):

    def __init__(self):
        self.driver_api = driverapi.API()
        self.perf_exporter = base_exporter.PerformanceExporterManager()

    def collect(self, ctx, task_instance_id):
        """
        :return:
        """
        result = constants.TaskExecutionResult.RUNNING
        try:
            task_instance = db.task_instance_get(context, task_instance_id)
            LOG.info('Collecting performance metrics for task_instance: %s'
                     % dict(task_instance))
            current_time = int(datetime.utcnow().timestamp()) * 1000
            task_instance['launch_time'] = current_time
            task_instance['result'] = result
            db.task_instance_update(context, task_instance_id, task_instance)

            # collect the performance metrics from driver and push to
            # prometheus exporter api
            end_time = current_time + task_instance['interval']
            perf_metrics = self.driver_api \
                .collect_perf_metrics(ctx, task_instance['storage_id'],
                                      task_instance['args'],
                                      current_time, end_time)

            self.perf_exporter.dispatch(context, perf_metrics)
        except Exception as e:
            LOG.error(e)
            msg = _("Failed to collect performance metrics for task instance "
                    "id:{0} ".format(task_instance_id))
            LOG.error(msg)
            result = constants.TaskExecutionResult.FAILED
        else:
            LOG.info("Performance metrics collection done for storage id :{0} "
                     "and task instance id:{1}"
                     .format(task_instance['storage_id'], task_instance_id))
            result = constants.TaskExecutionResult.SUCCEED

        # Update task execution result
        task_instance['result'] = result
        LOG.info("************Updated Task instance status*********")
        task_instance = dict(task_instance)
        for k in task_instance:
            LOG.info("%s : %s" % (k, task_instance[k]))
        LOG.info("***********************************************")

        db.task_instance_update(context, task_instance_id, task_instance)

        # Stop the job after end of collection task
        schedule = config.Scheduler.getInstance()
        job_id = task_instance_id
        if schedule.get_job(job_id):
            schedule.remove_job(job_id)
