from django.test import TestCase
from .models import Account
import uuid

class AccountModelTest(TestCase):
    
    def setUp(self):
        # Create two test accounts
        self.account1 = Account.objects.create(account_id=uuid.uuid4(), name="Test Account 1", balance=1000.00)
        self.account2 = Account.objects.create(account_id=uuid.uuid4(), name="Test Account 2", balance=500.00)
    
    def test_account_creation(self):
        # Test account creation
        self.assertEqual(self.account1.name, "Test Account 1")
        self.assertEqual(self.account2.balance, 500.00)
    
    def test_transfer_funds(self):
        # Test transferring funds between accounts
        self.account1.balance -= 100
        self.account2.balance += 100
        self.account1.save()
        self.account2.save()
        
        self.assertEqual(self.account1.balance, 900.00)
        self.assertEqual(self.account2.balance, 600.00)
