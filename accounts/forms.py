from django import forms
from .models import Account

class UploadFileForm(forms.Form):
    csv_file = forms.FileField()

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
