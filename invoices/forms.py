from django.forms import ModelForm, Textarea, widgets, DateInput
from invoices.models import Invoice


class DateField(DateInput):
    input_type = "date"


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            'date_receipt', 'date', 'no_invoice', 'doc_types', 'sum', 'date_of_payment', 'information', 'creation_date',
            'change_date', 'author')
        exclude = ['creation_date',
                   'change_date', 'author']
        labels = {'date_receipt': 'Data wpływu', 'date': 'Data wystawienia', 'no_invoice': 'Nr. dokumentu',
                  'doc_types': 'Rodzaj dokumentu', 'sum': 'Kwota faktury', 'date_of_payment': 'Data płatności',
                  'information': 'Informacje ', 'creation_date': 'Data utworzenia', 'change_date': 'Data zmian',
                  'author': 'Autor'
                  }
        widgets = {'information': Textarea(attrs={'rows': 3}),
                   'date': DateField(),
                   'date_receipt': DateField(),
                   'date_of_payment': DateField()
                   }
