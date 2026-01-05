from django.db import models

# Create your models here.
class Typecpv(models.Model):
    class Meta:
        verbose_name = "CPV"
        verbose_name_plural = "Słownik CPV"

    no_cpv = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.no_cpv}"
    
class Genre(models.Model):
    class Meta:
        verbose_name = "Klasyfikacja rodzajowa"
        verbose_name_plural = "Klasyfikacja rodzajowa"
        ordering = ["name_id"]

    name_id = models.CharField("ID", max_length=4, unique=True)
    name = models.CharField("Ogólna nazwa przedmiotu zamówienia w ujęciu rodzajowym", max_length=200)
    cpv = models.ManyToManyField(Typecpv, verbose_name="Kody CPV", related_name="Genre")

    def __str__(self):
        return f"({self.name_id}) {self.name}"
    
class OrderLimit(models.Model):
    class Meta:
        verbose_name = "Limit zamówień"
        verbose_name_plural = "Limit zamówień"
        ordering = ["-year"]

    year = models.IntegerField("Rok", unique=True)
    euro_exchange_rate = models.DecimalField("Kurs euro", max_digits=5, decimal_places=4)
    limit_euro = models.DecimalField("Limit euro", max_digits=10, decimal_places=2)
    limit_netto = models.DecimalField("Limit zamówień netto", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.year} - {self.euro_exchange_rate} ({self.limit_euro}) - {self.limit_netto}zł."