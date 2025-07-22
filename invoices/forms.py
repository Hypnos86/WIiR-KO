from django.forms import ModelForm, Textarea, widgets, DateInput
from django import forms
from invoices.models import Invoice, InvoiceItems


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            'date_receipt', 'date', 'no_invoice', 'doc_types', 'sum', 'date_of_payment', 'information',
            'creation_date', 'change_date', 'author')
        labels = {'date_receipt': 'Data wpływu', 'date': 'Data wystawienia', 'no_invoice': 'Nr. dokumentu',
                  'doc_types': 'Rodzaj dokumentu', 'sum': 'Kwota faktury', 'date_of_payment': 'Data płatności',
                  'information': 'Informacje ', 'creation_date': 'Data utworzenia', 'change_date': 'Data zmian',
                  'author': 'Autor'}
        exclude = ['creation_date', 'change_date', 'author']
        widgets = {'information': Textarea(attrs={'rows': 3}),
                   'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                   'date_receipt': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                   'date_of_payment': DateInput(attrs={'type': 'date', 'class': 'form-control'})
                   }


class InvoiceItemsForm(ModelForm):
    class Meta:
        model = InvoiceItems
        fields = (
            'invoice_id', 'contract_types', 'period_from', 'period_to', 'measurementSystemNumber', 'counterReading',
            'consumption', 'unit', 'section', 'group', 'paragraph', 'sum', 'information')
        labels = {'invoice_id': 'Faktura', 'period_from': 'Okres od', 'period_to': 'Okres do',
                  'contract_types': 'Rodzaj umowy', 'measurementSystemNumber': 'Nr. licznika',
                  'counterReading': 'Stan licznika', 'consumption': 'Zużycie', 'unit': 'Jednostka',
                  'section': 'Rozdział', 'group': 'Grupa', 'paragraph': 'Paragraf', 'sum': 'Kwota',
                  'infomation': 'Uwagi'}
        exclude = ['creation_date', 'invoice_id', 'section', 'group']
        widgets = {'period_from': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                   'period_to': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                   'information': Textarea(attrs={'rows': 1})
                   }
