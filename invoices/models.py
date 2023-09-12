from django.db import models
from enum import Enum
from units.models import Unit
import datetime


class DocumentsTypeEnum(Enum):
    FAKTURA = "Faktura"
    KOREKTA = "Korekta"


class DocumentTypes(models.Model):
    class Meta:
        verbose_name = "Rodzaj dokumentu księgowego"
        verbose_name_plural = "04 - Rodzaje dokumentów księgowych"

    type = models.CharField("Typ dokumentu", max_length=20)

    def __str__(self):
        return f"{self.type}"


class ContractTypes(models.Model):
    class Meta:
        verbose_name = "Rodzaj umowy"
        verbose_name_plural = "05 - Rodzaje umów"

    type = models.CharField("Typ dokumentu", max_length=20)

    def __str__(self):
        return f"{self.type}"


class Invoice(models.Model):
    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "07 - Faktury"
        ordering = ["-date_receipt"]

    related_name = "invoices"

    date_receipt = models.DateField("Data wpływu")
    date = models.DateField("Data wystawienia")
    no_invoice = models.CharField("Nr. faktury", max_length=30)
    doc_types = models.ForeignKey(DocumentTypes, null=False, blank=False, on_delete=models.CASCADE,
                                  verbose_name="Rodzaj dokumentu",
                                  related_name=related_name)
    sum = models.DecimalField("Kwota [zł]", max_digits=10, decimal_places=2, null=True, blank=True)
    date_of_payment = models.DateField("Termin płatności")
    type_contract = models.ForeignKey(ContractTypes, null=False, on_delete=models.CASCADE, related_name=related_name)
    information = models.TextField("Informacje", blank=True, null=True)
    creation_date = models.DateTimeField("Data utworzenia", auto_now_add=True)
    change_date = models.DateTimeField("Zmiana", auto_now=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name)
    slug = models.SlugField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.no_invoice} z dnia {self.date.strftime('%d.%m.%Y')} r."


class Section(models.Model):
    class Meta:
        verbose_name = "Rozdział"
        verbose_name_plural = "01 - Rozdziały"
        ordering = ["section"]

    section = models.CharField("Rozdział", max_length=5, unique=True)
    name = models.CharField("Nazwa", max_length=20)

    def __str__(self):
        return f"{self.section} ({self.name})"


class Group(models.Model):
    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "02 - Grupy"

    group = models.CharField("Grupa", max_length=2, unique=True)
    name = models.CharField("Nazwa", max_length=50)

    def __str__(self):
        return f"gr.{self.group}"


class Paragraph(models.Model):
    class Meta:
        verbose_name = "Paragraf i pozycja"
        verbose_name_plural = "03 - Paragrafy i pozycje"
        ordering = ['paragraph']

    paragraph = models.CharField("Paragraf", max_length=7, unique=True)
    name = models.CharField("Nazwa", max_length=50)

    def __str__(self):
        return f"{self.paragraph}"


class InvoiceItems(models.Model):
    class Meta:
        verbose_name = "Element faktury"
        verbose_name_plural = "06 - Elementy faktury"
        ordering = ["invoice_id"]

    related_name = "invoice_items"

    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='Faktura',
                                   related_name=related_name)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Jednostka', related_name=related_name)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Rozdział', related_name=related_name)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Grupa', related_name=related_name)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, verbose_name='Paragraf',
                                  related_name=related_name)
    sum = models.DecimalField("Kwota brutto [zł]", max_digits=10, decimal_places=2, null=True, blank=True)
    information = models.CharField(max_length=400, verbose_name='Uwagi')

    def __str__(self):
        return f"{self.section} - {self.group} - {self.paragraph} zł."
