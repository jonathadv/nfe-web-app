from django.core.management.base import BaseCommand
from django.db import connection

DATABASE = "nfeweb"
DATABASE_USER = "nfeweb"
DATABASE_PASSWORD = "nfeweb"


class Command(BaseCommand):
    help = "Create db schema"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {DATABASE};")
            cursor.execute(f"CREATE USER {DATABASE_USER} WITH PASSWORD '{DATABASE_PASSWORD}';")
            cursor.execute(f"ALTER ROLE {DATABASE} SET client_encoding TO 'utf8';")
            cursor.execute(
                f"ALTER ROLE {DATABASE_USER} SET default_transaction_isolation TO 'read committed';"
            )
            cursor.execute(f"ALTER ROLE {DATABASE} SET timezone TO 'UTC';")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE} TO {DATABASE_USER};")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Database '{DATABASE}' and user '{DATABASE_USER}' successfully created"
                )
            )
