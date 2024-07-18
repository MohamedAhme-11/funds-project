from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_accounts, name='list_accounts'),
    path('account/<uuid:account_id>/', views.account_detail, name='account_detail'),
    path('transfer/', views.transfer_funds, name='transfer_funds'),
    path('upload/', views.upload_accounts, name='upload_accounts'),
]
