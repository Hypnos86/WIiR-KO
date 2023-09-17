from django.urls import path, include
from invoices.views import InvoicesListView, NewInvoiceView, EditInvoiceView, InvoiceItemsView, InvoiceInfoView, \
    UnitCostListView

app_name = 'invoices'
urlpatterns = [
    path('list/', InvoicesListView.as_view(), name='listInvoice'),
    path('newInvoice/', NewInvoiceView.as_view(), name='newInvoice'),
    path('newInvoice/items/<slug:invoice_slug>/', InvoiceItemsView.as_view(), name='items'),
    path('editInvoice/<slug:invoice_slug>/', EditInvoiceView.as_view(), name='editInvoice'),
    path('infoInvoice/<int:id>/', InvoiceInfoView.as_view(), name='infoInvoice'),
    path('list/<slug:unit_slug>/<slug:paragraph_slug>/', UnitCostListView.as_view(), name='unitCostList'),

]
