from django.urls import path
from invoices.views import NewInvoiceView, EditInvoiceView, AddInvoiceItemsView, DeleteInvoiceView, \
    DeleteInvoiceItemView, CreateCSVForItems, EditInvoiceItemsView

app_name = 'invoices'
urlpatterns = [

    path('new/', NewInvoiceView.as_view(), name='newInvoice'),
    # path('new/items/<slug:invoiceSlug>/', NewInvoiceItemsView.as_view(), name='newItems'),
    path('edit/<slug:invoiceSlug>/', EditInvoiceView.as_view(), name='editInvoice'),
    path('add/items/<slug:invoiceSlug>/', AddInvoiceItemsView.as_view(), name='addItems'),
    path('edit/items/<slug:invoiceSlug>/<int:itemId>/', EditInvoiceItemsView.as_view(), name='editItems'),
    path("deleteInvoice/<slug:invoiceSlug>/", DeleteInvoiceView.as_view(), name="deleteInvoice"),
    path("deleteItem/<slug:invoiceSlug>/<int:item_id>", DeleteInvoiceItemView.as_view(), name="deleteInvoiceItem"),
    path("createCSV/<int:invoice_id>", CreateCSVForItems.as_view(), name="createFile"),

]
