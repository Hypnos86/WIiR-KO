from django.db import models


class County(models.Model):
    class Meta:
        verbose_name = "Powiat"
        verbose_name_plural = "J.01 - Powiaty"
        ordering = ["id_order"]

    swop_id = models.CharField(max_length=4, verbose_name="ID SWOP", unique=True)
    name = models.CharField(max_length=15, null=False, verbose_name="Powiat", unique=True)
    id_order = models.IntegerField("Kolejność", unique=True, null=True)

    def __str__(self):
        return f"{self.name}"
