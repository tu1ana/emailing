import json
from pathlib import Path

from django.core.management import BaseCommand

from main.models import Client, Emailing, Message


class Command(BaseCommand):

    def handle(self, *args, **options):

        Client.objects.all().delete()
        # Emailing.objects.all().delete()
        # Message.objects.all().delete()

        filepath = Path.cwd() / 'main.json'
        with open(filepath, encoding='utf-8') as f:
            data_list = json.load(f)

        clients_to_add = []
        # emailings_to_add = []
        # messages_to_add = []

        for data in data_list:
            data.pop('pk', None)
            if data['model'] == 'main.client':
                clients_to_add.append(Client(**data['fields']))
            # elif data['model'] == 'main.emailing':
            #     emailings_to_add.append(Emailing(**data['fields']))
            # elif data['model'] == 'main.message':
            #     messages_to_add.append(Message(**data['fields']))

        # print(clients_to_add)
        # print(emailings_to_add)
        # print(messages_to_add)

        Client.objects.bulk_create(clients_to_add)
        # Emailing.objects.bulk_create(emailings_to_add)
        # Message.objects.bulk_create(messages_to_add)
