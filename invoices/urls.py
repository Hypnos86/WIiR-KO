from django.urls import path
from invoices.views import NewInvoiceView, EditInvoiceView, AddInvoiceItemsView, DeleteInvoiceView, \
    DeleteInvoiceItemView, CreateCSVForItems, EditInvoiceItemsView, HandleRequestView

app_name = 'invoices'
urlpatterns = [
    path('new/', NewInvoiceView.as_view(), name='newInvoice'),
    path('<slug:invoiceSlug>/', EditInvoiceView.as_view(), name='editInvoice'),
    path('<slug:invoiceSlug>/item/', AddInvoiceItemsView.as_view(), name='addItems'),
    path('<slug:invoiceSlug>/item/<int:itemId>/', EditInvoiceItemsView.as_view(), name='editItems'),
    path("deleteInvoice/<slug:invoiceSlug>/", DeleteInvoiceView.as_view(), name="deleteInvoice"),
    path("deleteItem/<slug:invoiceSlug>/<int:item_id>", DeleteInvoiceItemView.as_view(), name="deleteInvoiceItem"),
    path("createCSV/<int:invoice_id>", CreateCSVForItems.as_view(), name="createFile"),
    path('<slug:invoiceSlug>/handle-request/', HandleRequestView.as_view(), name='handleRequest'),
]
