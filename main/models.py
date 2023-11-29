from django.db import models


# Create your models here.
class CountyCard(models.Model):
    class Meta:
        verbose_name = 'Jednostka powiatowa'
        verbose_name_plural = '01 - Nazwy kart'
        ordering = ['id_order']

    name = models.CharField(max_length=15, null=False, verbose_name="Jednostka powiatowa", unique=True)
    id_order = models.IntegerField(verbose_name="Kolejność", unique=True, null=True)
    slug = models.SlugField(max_length=20, null=True, blank=True)

    @classmethod
    def create_county_cards(cls):
        # Tworzenie listy danych, które mają być użyte do stworzenia obiektów
        data = [
            {"name": "KWP Poznań", "id_order": 1},
            {"name": "Chodzież", "id_order": 2},
            {"name": "Czarnków", "id_order": 3},
            {"name": "Gniezno", "id_order": 4},
            {"name": "Gostyń", "id_order": 5},
            {"name": "Grodzisk Wlkp.", "id_order": 6},
            {"name": "Jarocin", "id_order": 7},
            {"name": "Kalisz", "id_order": 8},
            {"name": "Kępno", "id_order": 9},
            {"name": "Koło", "id_order": 10},
            {"name": "Konin", "id_order": 11},
            {"name": "Koscian", "id_order": 12},
            {"name": "Krotoszyn", "id_order": 13},
            {"name": "Leszno", "id_order": 14},
            {"name": "Międzychód", "id_order": 15},
            {"name": "Nowy Tomyśl", "id_order": 16},
            {"name": "Oborniki", "id_order": 17},
            {"name": "Ostrów Wlkp.", "id_order": 18},
            {"name": "Ostrzeszów", "id_order": 19},
            {"name": "Piła", "id_order": 20},
            {"name": "Pleszew", "id_order": 21},
            {"name": "Poznań", "id_order": 22},
            {"name": "Rawicz", "id_order": 23},
            {"name": "Słupca", "id_order": 24},
            {"name": "Śrem", "id_order": 25},
            {"name": "Środa Wlkp.", "id_order": 26},
            {"name": "Szamotuły", "id_order": 27},
            {"name": "Turek", "id_order": 28},
            {"name": "Wągrowiec", "id_order": 29},
            {"name": "Wolsztyn", "id_order": 30},
            {"name": "Września", "id_order": 31},
            {"name": "Złotów", "id_order": 32},
        ]

        for item in data:
            county = cls(name=item["name"], id_order=item["id_order"])
            county.save()
        return cls.objects.all()

    def __str__(self):
        return f"{self.name}"


class HelpInfo(models.Model):
    class Meta:
        verbose_name = 'Informacja'
        verbose_name_plural = '02 - Informacje'

    related_name = "help_view"

    info = models.TextField(verbose_name='Informacja', null=True, blank=True)
    authorEmail = models.EmailField(verbose_name='Email')
    authorPhone = models.CharField(verbose_name='Telefon', max_length=9)
    create_date = models.DateField("Data dodania", auto_now_add=True)
    change = models.DateTimeField(auto_now=True, verbose_name="Zmiany")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name, verbose_name="Autor")

    @classmethod
    def create_support(cls):
        data = [{'authorEmail': 'kamil.kubiak@po.policja.gov.pl', 'authorPhone': '77-124-60', 'author': 1}]

        for item in data:
            support = cls(authorEmail=item["authorEmail"], authorPhone=item["authorPhone"], author_id=item["author"])
            support.save()
        return cls.objects.all()

    def __str__(self):
        return f'Informacja: {self.id}'
