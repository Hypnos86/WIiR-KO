from django.db import models
from main.models import CountyCard


class County(models.Model):
    class Meta:
        verbose_name = "Jednostka SWOP"
        verbose_name_plural = "Jednostki SWOP"
        ordering = ["id_order"]

    swop_id = models.CharField(max_length=4, verbose_name="ID SWOP")
    name = models.CharField(max_length=15, null=False, verbose_name="Jednostka", unique=True)
    id_order = models.IntegerField("Kolejność", unique=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.swop_id}"


class TypeUnit(models.Model):
    class Meta:
        verbose_name = "Rodzaj obiektu"
        verbose_name_plural = "Rodzaje obiektów"
        ordering = ["id"]

    type_short = models.CharField(max_length=30, null=False, verbose_name="Skrócona nazwa")
    type_full = models.CharField(max_length=100, null=False, verbose_name="Pełna nazwa")
    id_order = models.IntegerField("Kolejność", unique=True, null=True)

    def __str__(self):
        return f"{self.type_short}"


class Unit(models.Model):
    class Meta:
        verbose_name = "Obiekt"
        verbose_name_plural = "Obiekty"
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
    manager = models.CharField(max_length=150, verbose_name='Administrator', default='Policja')
    information = models.TextField(null=True, blank=True, verbose_name='Informacje')
    status = models.BooleanField(default=True, verbose_name='Aktualna')
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    change = models.DateTimeField(auto_now=True, verbose_name='Zmiany')
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name, verbose_name='Autor')

    def __str__(self):
        return f"{self.unit_full_name}"
