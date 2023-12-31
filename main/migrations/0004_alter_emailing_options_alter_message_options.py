# Generated by Django 4.2.6 on 2023-11-02 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_user_message_auth_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailing',
            options={'permissions': [('change_status', 'Can change status'), ('set_start_time', 'Can set start time'), ('set_finish_time', 'Can set finish time')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'permissions': [('view_all_messages', 'Can see all messages'), ('deactivate', 'Can deactivate messages')], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]
