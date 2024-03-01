import json
import logging

logger = logging.getLogger(__name__)
from django.core.management.base import BaseCommand

from ...models import UserData


def json_loader(filename):
    with open(f"projects/emaktabuz/management/commands/json/{filename}", "r") as file:
        return json.loads(file.read())


def add_data_to_bot_db(data):
    for user in data['users']:
        username = user.get('username', '')
        password = user.get('password', '')

        # Create or update UserData model instance
        user_instance, created = UserData.objects.update_or_create(
            login=username,
            defaults={
                'password': password,
                # Add other fields here if needed
            }
        )

        if created:
            print(f"User {username} added to the database.")
        else:
            print(f"User {username} updated in the database.")


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            user_data = json_loader("user_data.json")
            add_data_to_bot_db(user_data)

            print("Data loaded successfully")
        except Exception as e:
            logger.exception("Error occurred while loading data")
            print("An error occurred while loading data. Please check logs for more details.")
