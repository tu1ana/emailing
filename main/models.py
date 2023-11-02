from django.conf import settings
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Emailing(models.Model):

    FREQ_CHOICES = [
        ('DY', 'Раз в день'),
        ('WK', 'Раз в неделю'),
        ('MO', 'Раз в месяц'),
    ]
    # COMPLETE = 'COMPLETE'
    # CREATED = 'CREATED'
    # STARTED = 'STARTED'
    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('COMPLETE', 'Завершена')
    ]
    start_time = models.DateTimeField(verbose_name='Время рассылки')
    finish_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    freq = models.CharField(max_length=2, choices=FREQ_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='CREATED', verbose_name='Статус рассылки')

    # client = models.ManyToManyField(Client, verbose_name='Клиент')

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
    # message - models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name='Сообщение')

    def __str__(self):
        return f'Рассылка {self.pk} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            ('change_status', 'Can change status'),
            ('set_start_time', 'Can set start time'),
            ('set_finish_time', 'Can set finish time')
        ]


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Текст сообщения')

    client = models.ManyToManyField(Client, verbose_name='Клиент')
    emailing = models.ForeignKey(Emailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    is_active = models.BooleanField(default=True, verbose_name='Активная')
    job_id = models.CharField(max_length=250, default='', verbose_name='ID задачи')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

        permissions = [
            ('view_all_messages', 'Can see all messages'),
            ('deactivate', 'Can deactivate messages')
        ]


class Log(models.Model):
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки')
    server_response = models.CharField(max_length=250, **NULLABLE, verbose_name='Ответ почтового сервера')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.pk} {self.status} ({self.last_attempt})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
