import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from main.services import launch_scheduler

logger = logging.getLogger(__name__)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # add_jobs(scheduler)

        scheduler.add_job(
            launch_scheduler,
            kwargs={'scheduler': scheduler},
            trigger=CronTrigger(day="*"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        # logger.info(f'New added {id}')

        # for message in get_emailing():
        #     clients = list(message.client.all())
        #
        #     if message.emailing.sending_time:
        #         sending_time = message.emailing.sending_time
        #     else:
        #         sending_time = datetime.now()
        #
        #     if message.emailing.finish_time:
        #         finish_time = message.emailing.finish_time
        #     else:
        #         finish_time = sending_time + timedelta(days=365)
        #
        #     if message.emailing.freq == 'OAD':
        #         trigger = CronTrigger(second=sending_time.second,
        #                               minute=sending_time.minute,
        #                               hour=sending_time.hour,
        #                               start_date=sending_time,
        #                               end_date=finish_time
        #                               )
        #     elif message.emailing.freq == 'OAW':
        #         trigger = CronTrigger(second=sending_time.second,
        #                               minute=sending_time.minute,
        #                               hour=sending_time.hour,
        #                               day_of_week=sending_time.weekday(),
        #                               start_date=sending_time,
        #                               end_date=finish_time
        #                               )
        #     else:
        #         trigger = CronTrigger(second=sending_time.second,
        #                               minute=sending_time.minute,
        #                               hour=sending_time.hour,
        #                               day_of_week=sending_time.weekday(),
        #                               week=sending_time.week(),
        #                               start_date=sending_time,
        #                               end_date=finish_time
        #                               )
        #     scheduler.add_job(
        #         send_emailing,
        #         kwargs={'message': message, 'clients': clients},
        #         trigger=trigger,
        #         id=f'{message}',
        #         max_instances=1,
        #         replace_existing=True
        #     )
        #     logger.info(f'New added {id}')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
