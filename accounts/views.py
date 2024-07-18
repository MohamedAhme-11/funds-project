from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Account
from .forms import TransferForm, UploadFileForm
from django.core.files.storage import FileSystemStorage
import csv
import logging
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

def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/list_accounts.html', {'accounts': accounts})

def account_detail(request, account_id):
    account = get_object_or_404(Account, account_id=account_id)
    return render(request, 'accounts/account_detail.html', {'account': account})

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
