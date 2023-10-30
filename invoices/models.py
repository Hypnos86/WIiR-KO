from django.db import models
from enum import Enum
from units.models import Unit, County
from main.static_data import SECTION

sectionOptions = [(item['id'], item['section'], item['name']) for item in SECTION]


class DocumentsTypeEnum(Enum):
    FAKTURA = "Faktura"
    KOREKTA = "Korekta"


class DocumentTypes(models.Model):
    class Meta:
        verbose_name = "Rodzaj dokumentu księgowego"
        verbose_name_plural = "04 - Rodzaje dokumentów księgowych"

    type = models.CharField("Typ dokumentu", max_length=20)

    @classmethod
    def create_type(cls):
        data = [
            {"type": "Faktura"},
            {"type": "Korekta"},
            {"type": "Pismo"}
        ]

        for item in data:
            type = cls(type=item["type"])
            type.save()

        return cls.objects.all()

    def __str__(self):
        return f"{self.type}"


class ContractTypes(models.Model):
    class Meta:
        verbose_name = "Rodzaj umowy"
        verbose_name_plural = "05 - Rodzaje umów"

    type = models.CharField("Typ dokumentu", max_length=20)

    @classmethod
    def create_contract_types(cls):
        data = [
            {"type": "Nie dotyczy"},
            {"type": "Kompleksowa"},
            {"type": "OSD"},
            {"type": "Sprzedaż"}
        ]

        for item in data:
            type = cls(type=item["type"])
            type.save()

        return cls.objects.all()

    def __str__(self):
        return f"{self.type}"


class Invoice(models.Model):
    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "07 - Faktury"
        ordering = ["-date_receipt"]

    related_name = "invoice"

    date_receipt = models.DateField("Data wpływu")
    date = models.DateField("Data wystawienia")
    no_invoice = models.CharField("Nr. faktury", max_length=30)
    doc_types = models.ForeignKey(DocumentTypes, null=False, blank=False, on_delete=models.CASCADE,
                                  verbose_name="Rodzaj dokumentu",
                                  related_name=related_name)
    sum = models.DecimalField(verbose_name="Kwota [zł]", max_digits=10, decimal_places=2, null=True, blank=True)
    date_of_payment = models.DateField("Termin płatności")
    information = models.TextField("Informacje", blank=True, null=True)
    creation_date = models.DateTimeField("Data utworzenia", auto_now_add=True)
    change_date = models.DateTimeField("Zmiana", auto_now=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name, verbose_name='Autor')
    slug = models.SlugField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.no_invoice} z dnia {self.date.strftime('%d.%m.%Y')} r."


class Section(models.Model):
    class Meta:
        verbose_name = "Rozdział"
        verbose_name_plural = "01 - Rozdziały"
        ordering = ["section"]

    related_name = 'section'

    section = models.CharField(verbose_name="Rozdział", max_length=5, unique=True)
    name = models.CharField(verbose_name="Nazwa", max_length=20)
    swop_id = models.ManyToManyField(County, verbose_name="SWOP", blank=True, related_name=related_name)

    def __str__(self):
        return f"{self.section} ({self.name})"


class Group(models.Model):
    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "02 - Grupy"

    group = models.CharField("Grupa", max_length=2, unique=True)
    name = models.CharField("Nazwa", max_length=50)

    @classmethod
    def create_group(cls):
        data = [
            {"group": "6", "name": "Grupa 6 - Administracja i utrzymanie obiektów"}
        ]

        for item in data:
            groups = cls(group=item["group"], name=item["name"])
            groups.save()

        return cls.objects.all()

    def __str__(self):
        return f"gr.{self.group}"


class Paragraph(models.Model):
    class Meta:
        verbose_name = "Paragraf i pozycja"
        verbose_name_plural = "03 - Paragrafy i pozycje"
        ordering = ['paragraph']

    paragraph = models.CharField(verbose_name="Paragraf", max_length=7, unique=True)
    name = models.CharField(verbose_name="Nazwa", max_length=100)
    slug = models.SlugField(max_length=7, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.paragraph} - {self.name}"


class InvoiceItems(models.Model):
    class Meta:
        ordering = ["-creation_date"]
        verbose_name = "Element faktury"
        verbose_name_plural = "06 - Elementy faktury"

    related_name = "items"

    invoice_id = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, verbose_name='Faktura',
                                   related_name=related_name)
    contract_types = models.ForeignKey(to=ContractTypes, on_delete=models.CASCADE, verbose_name='Typ umowy')
    period_from = models.DateField(verbose_name='Okres od', null=False)
    period_to = models.DateField(verbose_name='Okres do', null=False)
    measurementSystemNumber = models.CharField(verbose_name='Nr. licznika', null=True, blank=True, max_length=15)
    # counterReading = models.DecimalField(verbose_name='Stan licznika', max_digits=10, decimal_places=2, null=True,
    counterReading = models.CharField(verbose_name='Stan licznika', max_length=80, null=True, blank=True)
    consumption = models.IntegerField(verbose_name='Zużycie', null=True, blank=True)
    unit = models.ForeignKey(to=Unit, on_delete=models.CASCADE, verbose_name='Jednostka', related_name=related_name)
    section = models.ForeignKey(to=Section, null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name='Rozdział',
                                related_name=related_name)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, verbose_name='Grupa', related_name=related_name)
    paragraph = models.ForeignKey(to=Paragraph, on_delete=models.CASCADE, verbose_name='Paragraf',
                                  related_name=related_name)
    sum = models.DecimalField(verbose_name="Kwota brutto [zł]", max_digits=10, decimal_places=2, null=False)
    information = models.TextField(verbose_name='Informacje', null=True, blank=True)
    creation_date = models.DateTimeField(verbose_name="Data utworzenia", auto_now_add=True)
    change_date = models.DateTimeField(verbose_name="Zmiana", auto_now=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name,
                               verbose_name='Autor')

    def __str__(self):
        return f"{self.section}-{self.group}-{self.paragraph}"
