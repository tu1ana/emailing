from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username} ({self.email})'

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = [
            ('view_all_users', 'Can see all users'),
            ('block_user', 'Can block users')
        ]
