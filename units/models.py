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

    # TODO stworzy reczna liste obiektow ktore ie zapisza po odpaleniu
    # @classmethod
    # def create_county_cards(cls):
    #     # Tworzenie listy danych, które mają być użyte do stworzenia obiektów
    #     data = [
    #         {"swop_id": "3200", "name": "KWP", "id_order": 1},
    #         {"swop_id": "3201", "name": "Chodzież", "id_order": 2},
    #         {"swop_id": "3202", "name": "Czarnków", "id_order": 3},
    #         {"swop_id": "3203", "name": "Gniezno", "id_order": 4},
    #         {"swop_id": "3204", "name": "Wartość1", "id_order": 5},
    #         {"swop_id": "3205", "name": "Wartość1", "id_order": 6},
    #         {"swop_id": "3206", "name": "Wartość1", "id_order": 7},
    #         {"swop_id": "3207", "name": "Wartość1", "id_order": 8},
    #         {"swop_id": "3208", "name": "Wartość1", "id_order": 9},
    #         {"swop_id": "3209", "name": "Wartość1", "id_order": 10},
    #         {"swop_id": "3210", "name": "Wartość1", "id_order": 11},
    #         {"swop_id": "3211", "name": "Wartość1", "id_order": 12},
    #         {"swop_id": "3212", "name": "Wartość1", "id_order": 13},
    #         {"swop_id": "3213", "name": "Wartość1", "id_order": 14},
    #         {"swop_id": "3214", "name": "Wartość1", "id_order": 15},
    #         {"swop_id": "3215", "name": "Wartość1", "id_order": 16},
    #         {"swop_id": "3216", "name": "Wartość1", "id_order": 17},
    #         {"swop_id": "3217", "name": "Wartość1", "id_order": 18},
    #         {"swop_id": "3218", "name": "Wartość1", "id_order": 19},
    #         {"swop_id": "3219", "name": "Wartość1", "id_order": 20},
    #         {"swop_id": "3220", "name": "Wartość1", "id_order": 21},
    #         {"swop_id": "3221", "name": "Wartość1", "id_order": 22},
    #         {"swop_id": "3222", "name": "Wartość1", "id_order": 23},
    #         {"swop_id": "3223", "name": "Wartość1", "id_order": 24},
    #         {"swop_id": "3224", "name": "Wartość1", "id_order": 25},
    #         {"swop_id": "3225", "name": "Wartość1", "id_order": 26},
    #         {"swop_id": "3226", "name": "Wartość1", "id_order": 27},
    #         {"swop_id": "3227", "name": "Wartość1", "id_order": 28},
    #         {"swop_id": "3228", "name": "Wartość1", "id_order": 29},
    #         {"swop_id": "3229", "name": "Wartość1", "id_order": 30},
    #         {"swop_id": "3230", "name": "Wartość1", "id_order": 31},
    #         {"swop_id": "3231", "name": "Wartość1", "id_order": 32},
    #         {"swop_id": "3232", "name": "Wartość1", "id_order": 33},
    #         {"swop_id": "3233", "name": "Wartość1", "id_order": 34}
    #     ]
    #
    #     # Tworzenie i zapisywanie obiektów w pętli
    #     for item in data:
    #         county = cls(swop_id=item["swop_id"], name=item["name"], id_order=item["id_order"])
    #         county.save()
    #
    #     return cls.objects.all()

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

    def __str__(self):
        return f"{self.type_full}"


# class CostType(models.Model):
#     class Meta:
#         verbose_name = "Rodzaj kosztów"
#         verbose_name_plural = "03 - Karty Rodzajów kosztów"
#         # ordering = ["county_swop__swop_id", "type"]
#
#     related_name = "costType"
#
#     name = models.CharField(max_length=40, verbose_name='Rodzaj kosztu')
#
#     def __str__(self):
#         return f"{self.name}"


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
