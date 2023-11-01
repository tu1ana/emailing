from django import template

from config import settings

register = template.Library()


@register.filter()
def my_media(value):
    if value:
        return f'{settings.MEDIA_URL}{value}'
    return f'/{settings.STATIC_URL}default-image.jpg'
