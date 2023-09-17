from django.urls import path, include
from invoices.views import NewInvoiceView, EditInvoiceView, NewInvoiceItemsView, EditInvoiceItemsView

app_name = 'invoices'
urlpatterns = [

    path('new/', NewInvoiceView.as_view(), name='newInvoice'),
    path('new/items/<slug:invoiceSlug>/', NewInvoiceItemsView.as_view(), name='newItems'),
    path('edit/<slug:invoiceSlug>/', EditInvoiceView.as_view(), name='editInvoice'),
    path('edit/items/<slug:invoiceSlug>/', EditInvoiceItemsView.as_view(), name='editItems'),

]
