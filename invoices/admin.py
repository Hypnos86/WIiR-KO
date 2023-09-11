from django.contrib import admin
from invoices.models import DocumentTypes, Invoice, Section, Group, Paragraph, ContractTypes

# Register your models here.
admin.site.register(Section)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group', 'name']


@admin.register(Paragraph)
class DocumentTypesAdmin(admin.ModelAdmin):
    list_display = ['paragraph', 'name']


@admin.register(DocumentTypes)
class DocumentTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']


@admin.register(ContractTypes)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['type']


@admin.register(Invoice)
class InvoiceBuyAdmin(admin.ModelAdmin):
    list_display = ['date_receipt', 'date', 'no_invoice', 'sum', 'creation_date',
                    'author']
    list_display_links = ['no_invoice']
    search_fields = ['no_invoice']
    search_help_text = "Szukaj po: nr. faktury"
