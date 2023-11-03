from django.conf import settings
from django.db import models
from django.utils import timezone

from main.models import NULLABLE
from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    article = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    pub_date = models.DateTimeField(default=timezone.now, **NULLABLE, verbose_name='Дата публикации')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Автор')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
