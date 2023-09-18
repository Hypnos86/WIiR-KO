from django.urls import path, include
from invoices.views import NewInvoiceView, EditInvoiceView, AddInvoiceItemsView, \
    DeleteInvoiceItemView

app_name = 'invoices'
urlpatterns = [

    path('new/', NewInvoiceView.as_view(), name='newInvoice'),
    # path('new/items/<slug:invoiceSlug>/', NewInvoiceItemsView.as_view(), name='newItems'),
    path('edit/<slug:invoiceSlug>/', EditInvoiceView.as_view(), name='editInvoice'),
    path('add/items/<slug:invoiceSlug>/', AddInvoiceItemsView.as_view(), name='addItems'),
    path("deleteItem/<slug:invoiceSlug>/<int:item_id>", DeleteInvoiceItemView.as_view(), name="deleteInvoiceItem"),

]
