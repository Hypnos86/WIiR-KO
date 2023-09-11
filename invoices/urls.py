from django.urls import path, include
from invoices.views import InvoicesListView, NewInvoiceView, InvoiceItemsView

app_name = 'invoices'
urlpatterns = [
    path('list/', InvoicesListView.as_view(), name='listInvoice'),
    path('newInvoice/', NewInvoiceView.as_view(), name='newInvoice'),
    path('newInvoice/items/<slug:invoice_slug>', InvoiceItemsView.as_view(), name='items')
]
