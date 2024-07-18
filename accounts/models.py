from django.db import models
import uuid

class Account(models.Model):
    # Primary key as a UUID for unique identification of each account
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Name of the account holder
    name = models.CharField(max_length=100)
    # Account balance with a maximum of 10 digits and 2 decimal places
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # String representation of the account showing name and ID
        return f"{self.name} ({self.account_id})"
