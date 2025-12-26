from django.contrib import admin
from invoices.models import DocumentTypes, Invoice, Section, Group, Paragraph, ContractTypes, InvoiceItems
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportMixin


# Register your models here.

@admin.register(Section)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['section', 'name']
    filter_horizontal = ['swop_id']


class InvoiceItemsResource(resources.ModelResource):
    invoice_id = Field(attribute='invoice_id', column_name='Faktura')
    period_from = Field(attribute='period_from', column_name='Od')
    period_to = Field(attribute='period_to', column_name='Do')
    measurementSystemNumber = Field(attribute='measurementSystemNumber', column_name='Nr. licznika')
    counterReading = Field(attribute='counterReading', column_name='Stan licznika')
    consumption = Field(attribute='consumption', column_name='Zużycie')
    combined_section_group_paragraph = Field(column_name='Rodział/Grupa/Paragraf')
    sum = Field(attribute='sum', column_name='Kwota')
    unit = Field(attribute='unit', column_name='Jednostka')
    information = Field(attribute='information', column_name='Informacje')

    def dehydrate_combined_section_group_paragraph(self, invoice_item):
        return f"{invoice_item.section.section}-{invoice_item.group.group}-{invoice_item.paragraph.paragraph}"

    class Meta:
        model = InvoiceItems
        fields = ('invoice_id', 'period_from', 'period_to', 'measurementSystemNumber', 'counterReading', 'consumption',
                'combined_section_group_paragraph', 'sum', 'unit', 'information')
        export_order = (
            'invoice_id', 'period_from', 'period_to', 'measurementSystemNumber', 'counterReading', 'consumption',
            'combined_section_group_paragraph', 'sum', 'unit', 'information')


@admin.register(InvoiceItems)
class GroupAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'invoice_id', 'unit', 'section', 'group', 'paragraph_number', 'sum','author_full_name']
    search_fields = ['invoice_id__no_invoice', 'unit__city', 'unit__county_swop__name', 'paragraph__paragraph', 'sum', 'author__first_name', 'author__last_name' ]
    search_help_text = 'Szukaj po nr. faktury'
    autocomplete_fields = ['invoice_id', 'unit']
    resource_class = InvoiceItemsResource
    
    def author_full_name(self, obj):
        user = obj.author
        if not user:
            return '-'
        full_name = user.get_full_name() or user.username
        return full_name

    author_full_name.short_description = "Autor"
    
    def paragraph_number(self, obj):
        if not obj.paragraph:
            return '-'
        return obj.paragraph.paragraph

    paragraph_number.short_description = "Paragraf"


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
    list_display = ['id', 'type']


class InvoiceResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Identyfikator')
    date_receipt = Field(attribute='date_receipt', column_name='Data wpływu')
    date = Field(attribute='date', column_name='Data wystawienia')
    no_invoice = Field(attribute='no_invoice', column_name='Nr. Dokumentu')
    sum = Field(attribute='sum', column_name='Kwota')
    doc_types = Field(attribute='doc_types', column_name='Rodzaj dokumentu')
    date_of_payment = Field(attribute='date_of_payment', column_name='Data płatności')
    information = Field(attribute='information', column_name='Infomracje')

    class Meta:
        model = Invoice
        fields = ('id', 'date_receipt', 'date', 'no_invoice', 'doc_types', 'sum', 'date_of_payment', 'information')
        export_order = (
            'id', 'date_receipt', 'date', 'no_invoice', 'sum', 'date_of_payment', 'doc_types', 'information')


@admin.register(Invoice)
class CountyAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'date_receipt', 'date', 'no_invoice', 'sum', 'creation_date',
                    'author_full_name']
    list_display_links = ['no_invoice']
    search_fields = ['no_invoice', 'author__first_name', 'author__last_name']
    search_help_text = "Szukaj po: nr. faktury"
    resource_class = InvoiceResource
    
    def author_full_name(self, obj):
        user = obj.author
        if not user:
            return '-'
        full_name = user.get_full_name() or user.username
        return full_name

    author_full_name.short_description = "Autor"
