from datetime import datetime
from smtplib import SMTPException

from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils.timezone import now

from django.conf import settings
from main.models import Message, Client, Emailing, Log


def send_message(message: Message):

    for client in Client.objects.filter(message=message):
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            log = Log.objects.create(last_attempt=datetime.now(),
                                     server_response='Сообщение успешно отправлено',
                                     status='Success',
                                     message=message)
            log.save()
        except SMTPException as e:
            log = Log.objects.create(last_attempt=datetime.now(),
                                     server_response=e.args,
                                     status='Error',
                                     message=message)
            log.save()


def create_task(scheduler, message: Message):
    message.job_id = f'Задача {message.pk}'
    message.save()

    start_time = message.emailing.start_time
    finish_time = message.emailing.finish_time

    if message.emailing.freq == 'DY':
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              start_date=start_time,
                              end_date=finish_time
                              )
    elif message.emailing.freq == 'WK':
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              day_of_week=start_time.weekday,
                              start_date=start_time,
                              end_date=finish_time
                              )
    else:
        trigger = CronTrigger(second=start_time.second,
                              minute=start_time.minute,
                              hour=start_time.hour,
                              day_of_week=start_time.weekday,
                              week=start_time.week,
                              start_date=start_time,
                              end_date=finish_time
                              )
    scheduler.add_job(
        send_message,
        kwargs={'message': message},
        trigger=trigger,
        id=message.job_id,
        max_instances=1,
        replace_existing=True
    )


def check_time(message: Message):
    if now() <= message.emailing.finish_time:
        if now() >= message.emailing.start_time:
            message.emailing.status = 'STARTED'
            message.emailing.save()

            log = Log.objects.create(server_response='-', status='Запущена', message=message)
            log.save()
            return True
        else:
            return False
    else:
        message.emailing.status = 'COMPLETE'
        message.emailing.save()

        log = Log.objects.create(server_response='-', status='Завершена', message=message)
        log.save()
        return False


def launch_scheduler(scheduler):
    messages = Message.objects.filter(is_active=True)

    if messages:
        for message in messages:
            if message.emailing.status != 'COMPLETE':
                job_id = f'{message.pk}'
                if check_time(message):
                    if not scheduler.get_job(job_id):
                        create_task(scheduler, message)
                else:
                    if scheduler.get_job(job_id):
                        scheduler.pause_job(job_id)

        if scheduler.state == 0:
            scheduler.start()
