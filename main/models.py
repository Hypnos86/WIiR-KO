from django.db import models


# Create your models here.
class CountyCard(models.Model):
    class Meta:
        verbose_name = 'Jednostka powiatowa'
        verbose_name_plural = 'Jednostki powiatowe'
        ordering = ['id_order']

    name = models.CharField(max_length=15, null=False, verbose_name="Jednostka powiatowa", unique=True)
    id_order = models.IntegerField("Kolejność", unique=True, null=True)
    slug = models.SlugField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class HelpInfo(models.Model):
    class Meta:
        verbose_name = 'Informacja'
        verbose_name_plural = 'Informacje'

    related_name = "help_view"

    information = models.TextField('Informacja')
    create_date = models.DateField("Data dodania", auto_now_add=True)
    change = models.DateTimeField(auto_now=True, verbose_name="Zmiany")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name, verbose_name="Autor")

    def __str__(self):
        return f'Informacja: {self.id}'
