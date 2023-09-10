from django.forms import ModelForm, Textarea, widgets
from units.models import Unit


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ('county_unit', 'county_swop', 'type', 'address', 'zip_code', 'city', 'object_name', 'unit_full_name',
                  'manager', 'status', 'slug', 'information', 'change', 'author')
        exclude = ['unit_full_name', 'slug', 'change', 'author']
        labels = {'county_unit': 'Karta',
                  'county_swop': 'SWOP',
                  'type': 'Rodzaj jednostki',
                  'address': 'Adres',
                  'zip_code': 'Kod pocztowy',
                  'city': 'Miasto',
                  'object_name': 'Nazwa obiektu',
                  'manager': 'Administrator obiektu',
                  'status': 'Status jednostki',
                  'information': 'Informacje',
                  'change': 'Zmiany',
                  'author': 'Autor'
                  }
        widgets = {'information': Textarea(attrs={'rows': 3}),
                   'zip_code': widgets.TextInput(attrs={'pattern': '^[0-9]{2}-[0-9]{3}$', 'placeholder': '00-000'}),
                   }
