from django.contrib import admin

from main.models import Client, Message, Emailing, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')


@admin.register(Emailing)
class EmailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'finish_time', 'freq', 'status')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'status', 'server_response', 'message')
