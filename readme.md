# 📊 Account Transfer Application

This application manages account creation, fund transfers, and account data upload via CSV files using Django.

## 🏦 Models

### `Account`

- **📥 Imports:**
  - `from django.db import models`: Provides the necessary classes and functions for Django models.
  - `import uuid`: Generates universally unique identifiers (UUID).

- **🏷️ Fields:**
  - `account_id`: A primary key field using UUID for unique identification of each account.
    ```python
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ```
  - `name`: A CharField for storing the account holder's name, with a maximum length of 100 characters.
    ```python
    name = models.CharField(max_length=100)
    ```
  - `balance`: A DecimalField to store the account balance, with a maximum of 10 digits and 2 decimal places.
    ```python
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    ```

- **🔍 Methods:**
  - `__str__`: Returns a string representation of the account, showing the name and account ID.
    ```python
    def __str__(self):
        return f"{self.name} ({self.account_id})"
    ```

## 🧪 Tests

### `AccountModelTest`

- **📥 Imports:**
  - `from django.test import TestCase`: Provides a test case class for writing unit tests.
  - `from .models import Account`: Imports the `Account` model.
  - `import uuid`: Generates UUIDs for creating test accounts.

- **🔍 Methods:**
  - `setUp`: Creates two test accounts.
    ```python
    def setUp(self):
        self.account1 = Account.objects.create(account_id=uuid.uuid4(), name="Test Account 1", balance=1000.00)
        self.account2 = Account.objects.create(account_id=uuid.uuid4(), name="Test Account 2", balance=500.00)
    ```
  - `test_account_creation`: Tests account creation.
    ```python
    def test_account_creation(self):
        self.assertEqual(self.account1.name, "Test Account 1")
        self.assertEqual(self.account2.balance, 500.00)
    ```
  - `test_transfer_funds`: Tests transferring funds between accounts.
    ```python
    def test_transfer_funds(self):
        self.account1.balance -= 100
        self.account2.balance += 100
        self.account1.save()
        self.account2.save()
        
        self.assertEqual(self.account1.balance, 900.00)
        self.assertEqual(self.account2.balance, 600.00)
    ```

## 🖼️ Views

### `upload_accounts`

- **📥 Imports:**
  - `from django.shortcuts import render, redirect`: Provides shortcuts for rendering templates and redirecting.
  - `from django.core.files.storage import FileSystemStorage`: Handles file storage.
  - `from .models import Account`: Imports the `Account` model.
  - `from .forms import UploadFileForm`: Imports the form for file uploads.
  - `import csv`: Provides functionality for reading CSV files.
  - `import logging`: Provides logging functionality.

- **🔍 Functionality:**
  - Handles the upload and processing of CSV files to create `Account` objects.
    ```python
    def upload_accounts(request):
        if request.method == 'POST' and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'accounts/upload_accounts.html', {'error': 'This is not a CSV file'})

            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)

            with open(fs.path(filename), newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    account_id = row.get('ID')
                    name = row.get('Name')
                    balance = row.get('Balance')

                    if not account_id or not name or not balance:
                        logging.error(f"Missing fields in row: {row}")
                        return render(request, 'accounts/upload_accounts.html', {'error': 'Missing fields in CSV file'})

                    try:
                        balance = float(balance)
                    except ValueError:
                        logging.error(f"Invalid balance value in row: {row}")
                        return render(request, 'accounts/upload_accounts.html', {'error': 'Invalid balance value in CSV file'})

                    Account.objects.create(
                        account_id=account_id,
                        name=name,
                        balance=balance
                    )

            return redirect('list_accounts')
        else:
            form = UploadFileForm()
        return render(request, 'accounts/upload_accounts.html', {'form': form})
    ```

### `list_accounts`

- **📥 Imports:**
  - `from django.shortcuts import render`: Provides shortcut for rendering templates.
  - `from .models import Account`: Imports the `Account` model.

- **🔍 Functionality:**
  - Renders a list of all accounts.
    ```python
    def list_accounts(request):
        accounts = Account.objects.all()
        return render(request, 'accounts/list_accounts.html', {'accounts': accounts})
    ```

### `account_detail`

- **📥 Imports:**
  - `from django.shortcuts import render, get_object_or_404`: Provides shortcuts for rendering templates and getting objects or returning 404.
  - `from .models import Account`: Imports the `Account` model.

- **🔍 Functionality:**
  - Renders details of a specific account.
    ```python
    def account_detail(request, account_id):
        account = get_object_or_404(Account, account_id=account_id)
        return render(request, 'accounts/account_detail.html', {'account': account})
    ```

### `transfer_funds`

- **📥 Imports:**
  - `from django.shortcuts import render, redirect`: Provides shortcuts for rendering templates and redirecting.
  - `from .forms import TransferForm`: Imports the form for transferring funds.

- **🔍 Functionality:**
  - Handles the transfer of funds between accounts.
    ```python
    def transfer_funds(request):
        if request.method == 'POST':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']
                if from_account.balance < amount:
                    return render(request, 'accounts/transfer_funds.html', {'form': form, 'error': 'Insufficient funds'})
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                return redirect('list_accounts')
        else:
            form = TransferForm()
        return render(request, 'accounts/transfer_funds.html', {'form': form})
    ```

## 🔗 URLs

- **📥 Imports:**
  - `from django.urls import path`: Provides the `path` function for URL routing.
  - `from . import views`: Imports the views from the current app.

- **🛤️ URL Patterns:**
  - Maps URLs to their corresponding views.
    ```python
    urlpatterns = [
        path('', views.list_accounts, name='list_accounts'),
        path('account/<uuid:account_id>/', views.account_detail, name='account_detail'),
        path('transfer/', views.transfer_funds, name='transfer_funds'),
        path('upload/', views.upload_accounts, name='upload_accounts'),
    ]
    ```

## 📑 Forms

### `UploadFileForm`

- **📥 Imports:**
  - `from django import forms`: Provides the base form classes.

- **📄 Form Fields:**
  - `csv_file`: A file field for uploading CSV files.
    ```python
    class UploadFileForm(forms.Form):
        csv_file = forms.FileField()
    ```

### `TransferForm`

- **📥 Imports:**
  - `from django import forms`: Provides the base form classes.
  - `from .models import Account`: Imports the `Account` model.

- **📄 Form Fields:**
  - `from_account`: A ModelChoiceField for selecting the account to transfer funds from.
    ```python
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    ```
  - `to_account`: A ModelChoiceField for selecting the account to transfer funds to.
    ```python
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    ```
  - `amount`: A DecimalField for specifying the amount to transfer.
    ```python
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    ```

## 🛠️ Admin

### `urls.py`

- **📥 Imports:**
  - `from django.contrib import admin`: Provides the admin site.
  - `from django.urls import include, path`: Provides functions for URL routing.

- **🛤️ URL Patterns:**
  - Includes the admin site and the URLs from the accounts app.
    ```python
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('accounts.urls')),
    ]
    ```

## 📋 Requirements


# 🗃️ Project Setup Guide and Requirements 📋

## 🗃️ Libraries
- **Django**: A high-level Python web framework.

```sh
pip install django
UUID: A module for generating universally unique identifiers (comes with Python standard library).
🛠️ Steps to Run the Project
1. Clone the Repository
sh
Copy code
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
2. Create a Virtual Environment
sh
Copy code
python -m venv venv
3. Activate the Virtual Environment
On Windows:

sh
Copy code
venv\Scripts\activate
On macOS and Linux:

sh
Copy code
source venv/bin/activate
4. Install the Required Libraries
sh
Copy code
pip install django
5. Create and Apply Migrations
sh
Copy code
python manage.py makemigrations
python manage.py migrate
6. Run the Development Server
sh
Copy code
python manage.py runserver
7. Access the Application
Open your web browser and go to http://127.0.0.1:8000/.

8. Create a Superuser (Optional, for Accessing Django Admin)
sh
Copy code
python manage.py createsuperuser
9. Log in to the Admin Site
Open your web browser and go to http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

📄 Use the Application
Upload accounts via CSV by navigating to http://127.0.0.1:8000/accounts/upload/.
List all accounts by navigating to http://127.0.0.1:8000/accounts/.
View account details and transfer funds using the provided URLs and forms.
sql
Copy code

Feel free to copy this into your project's README file!