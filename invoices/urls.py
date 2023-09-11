from django.urls import path, include
from invoices.views import InvoicesView, NewInvoiceView

app_name = 'invoices'
urlpatterns = [
    path('list/', InvoicesView.as_view(), name='listInvoice'),
    path('newInvoice/', NewInvoiceView.as_view(), name='newInvoice')
]
