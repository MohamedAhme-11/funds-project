import csv
import uuid
from django.core.management.base import BaseCommand
from accounts.models import Account

class Command(BaseCommand):
    help = 'Import accounts from a CSV file'

    def add_arguments(self, parser):
        # Argument to specify the CSV file path
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        # Get the CSV file path from the arguments
        csv_file = kwargs['csv_file']
        # Open the CSV file for reading
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            # Iterate over each row in the CSV file
            for row in reader:
                # Create a new Account object for each row
                Account.objects.create(
                    account_id=uuid.UUID(row['ID']),
                    name=row['Name'],
                    balance=row['Balance']
                )
        self.stdout.write(self.style.SUCCESS('Accounts imported successfully'))
