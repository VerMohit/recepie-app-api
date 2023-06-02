"""
Custom Django command to wait for DB to be available
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError

# Error thrown by django when DB is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for DB"""

    def handle(self, *args, **options):
        """Entry point for command"""

        # Shows message to stdout
        self.stdout.write('Waiting for database...')

        # Assuming DB is not up until is is
        db_up = False

        while db_up is False:
            try:
                # If DB is not ready, throw an exception
                self.check(databases=['default'])
                # If no exception raised, DB is ready
                db_up = True
            except(Psycopg2OpError, OperationalError):
                # If try block throws error, display error to stdout
                self.stdout.write('Database unavailable, waiting 1 second...')
                # Wait for 1 second and try access DB again
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
