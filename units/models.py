from django.db import models
from main.models import CountyCard


class County(models.Model):
    class Meta:
        verbose_name = "Jednostka SWOP"
        verbose_name_plural = "01 - Jednostki (SWOP)"
        ordering = ["id_order"]

    swop_id = models.CharField(max_length=4, verbose_name="ID SWOP")
    name = models.CharField(max_length=15, null=False, verbose_name="Jednostka", unique=True)
    id_order = models.IntegerField(verbose_name="Kolejność", unique=True, null=True)

    @classmethod
    def create_county(cls):
        # Tworzenie listy danych, które mają być użyte do stworzenia obiektów
        data = [
            {"swop_id": "3200", "name": "KWP", "id_order": 1},
            {"swop_id": "3201", "name": "Chodzież", "id_order": 2},
            {"swop_id": "3202", "name": "Czarnków", "id_order": 3},
            {"swop_id": "3203", "name": "Gniezno", "id_order": 4},
            {"swop_id": "3204", "name": "Gostyń", "id_order": 5},
            {"swop_id": "3205", "name": "Grodzisk Wlkp.", "id_order": 6},
            {"swop_id": "3206", "name": "Jarocin", "id_order": 7},
            {"swop_id": "3207", "name": "Kalisz", "id_order": 8},
            {"swop_id": "3208", "name": "Kępno", "id_order": 9},
            {"swop_id": "3209", "name": "Koło", "id_order": 10},
            {"swop_id": "3210", "name": "Konin", "id_order": 11},
            {"swop_id": "3211", "name": "Koscian", "id_order": 12},
            {"swop_id": "3212", "name": "Krotoszyn", "id_order": 13},
            {"swop_id": "3213", "name": "Leszno", "id_order": 14},
            {"swop_id": "3214", "name": "Międzychód", "id_order": 15},
            {"swop_id": "3215", "name": "Nowy Tomyśl", "id_order": 16},
            {"swop_id": "3216", "name": "Oborniki", "id_order": 17},
            {"swop_id": "3217", "name": "Ostrów Wlkp.", "id_order": 18},
            {"swop_id": "3218", "name": "Ostrzeszów", "id_order": 19},
            {"swop_id": "3219", "name": "Piła", "id_order": 20},
            {"swop_id": "3220", "name": "Pleszew", "id_order": 21},
            {"swop_id": "3221", "name": "Poznań", "id_order": 22},
            {"swop_id": "3222", "name": "Rawicz", "id_order": 23},
            {"swop_id": "3223", "name": "Słupca", "id_order": 24},
            {"swop_id": "3224", "name": "Śrem", "id_order": 25},
            {"swop_id": "3225", "name": "Środa Wlkp.", "id_order": 26},
            {"swop_id": "3226", "name": "Szamotuły", "id_order": 27},
            {"swop_id": "3227", "name": "Turek", "id_order": 28},
            {"swop_id": "3228", "name": "Wągrowiec", "id_order": 29},
            {"swop_id": "3229", "name": "Wolsztyn", "id_order": 30},
            {"swop_id": "3230", "name": "Września", "id_order": 31},
            {"swop_id": "3231", "name": "Złotów", "id_order": 32},
        ]

        # Tworzenie i zapisywanie obiektów w pętli
        for item in data:
            county = cls(swop_id=item["swop_id"], name=item["name"], id_order=item["id_order"])
            county.save()

        return cls.objects.all()

    def __str__(self):
        return f"{self.name} - {self.swop_id}"


class TypeUnit(models.Model):
    class Meta:
        verbose_name = "Rodzaj obiektu"
        verbose_name_plural = "02 - Rodzaje obiektów"
        ordering = ["id"]

    type_short = models.CharField(max_length=30, null=False, verbose_name="Skrócona nazwa")
    type_full = models.CharField(max_length=100, null=False, verbose_name="Pełna nazwa")
    id_order = models.IntegerField("Kolejność", unique=True, null=True)

    @classmethod
    def create_type_unit(cls):
        # Tworzenie listy danych, które mają być użyte do stworzenia obiektów
        data = [
            {"type_short": "KWP", "type_full": "Komenda Wojewódzka Policji", "id_order": 1},
            {"type_short": "KMP", "type_full": "Komenda Miejska Policji", "id_order": 2},
            {"type_short": "KPP", "type_full": "Komenda Powiatowa Policji", "id_order": 3},
            {"type_short": "KP", "type_full": "Komisariat Policji", "id_order": 4},
            {"type_short": "PP", "type_full": "Posterunek Policji", "id_order": 5},
            {"type_short": "RD", "type_full": "Rewir Dzielnicowych", "id_order": 6},
            {"type_short": "PPD", "type_full": "Punkt Przyjęć Dzielnicowych", "id_order": 7},
            {"type_short": "PPI", "type_full": "Punkt Przyjęć Interesantów", "id_order": 8},
            {"type_short": "Ant.", "type_full": "Antena", "id_order": 9},
            {"type_short": "Inne", "type_full": "Inne", "id_order": 10},
        ]

        # Tworzenie i zapisywanie obiektów w pętli
        for item in data:
            typeUnit = cls(type_short=item["type_short"], type_full=item["type_full"], id_order=item["id_order"])
            typeUnit.save()

        return cls.objects.all()

    def __str__(self):
        return f"{self.type_full}"


class Unit(models.Model):
    class Meta:
        verbose_name = "Obiekt"
        verbose_name_plural = "04 - Obiekty"
        ordering = ["county_swop__swop_id", "type"]

    related_name = "unit"

    county_unit = models.ForeignKey(CountyCard, on_delete=models.CASCADE, related_name=related_name,
                                    verbose_name='Powiat')
    county_swop = models.ForeignKey(County, on_delete=models.CASCADE, related_name=related_name,
                                    verbose_name='Jednostka SWOP')
    type = models.ForeignKey(TypeUnit, on_delete=models.CASCADE, related_name=related_name,
                             verbose_name='Rodzaj obiektu')
    address = models.CharField(max_length=50, verbose_name='Adres')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    city = models.CharField(max_length=40, verbose_name='Miasto')
    unit_full_name = models.CharField(max_length=200, blank=True, verbose_name='Obiekt')
    object_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nazwa obiektu')
    manager = models.CharField(max_length=150, verbose_name='Administrator', default='Policja')
    information = models.TextField(null=True, blank=True, verbose_name='Informacje')
    status = models.BooleanField(default=True, verbose_name='Aktualna')
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    change = models.DateTimeField(auto_now=True, verbose_name='Zmiany')
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name, verbose_name='Autor')

    def __str__(self):
        return f"{self.unit_full_name}"
