from django.db import models


# Create your models here.
class CountyCard(models.Model):
    class Meta:
        verbose_name = 'Jednostka powiatowa'
        verbose_name_plural = 'Jednostki powiatowe'
        ordering = ['id_order']

    name = models.CharField(max_length=15, null=False, verbose_name="Jednostka powiatowa", unique=True)
    id_order = models.IntegerField("Kolejność", unique=True, null=True)

    def __str__(self):
        return f"{self.name}"
