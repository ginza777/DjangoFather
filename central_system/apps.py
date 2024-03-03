
from django.apps import AppConfig
from django.db import connection
from django.db.utils import ProgrammingError




def create_superuser_automatic(username, email, password):
    if "auth_user" in connection.introspection.table_names():
        try:
            from django.contrib.auth.models import User

            # Check if the user already exists
            if not User.objects.filter(username=username).exists():
                # Create a new superuser
                User.objects.create_superuser(username, email, password)
                print(f"Superuser '{username}' created successfully.")
            else:
                print(f"Superuser '{username}' already exists.")
        except ProgrammingError:
            print("you must migrate")


class CentralSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'central_system'

    def ready(self):
        import environ
        env = environ.Env()
        env.read_env(".env")
        username = env.str("SUPERUSER_USERNAME")
        email = env.str("SUPERUSER_EMAIL")
        password = env.str("SUPERUSER_PASSWORD")
        print(f"Creating superuser '{username}'...")
        create_superuser_automatic(username, email, password)
