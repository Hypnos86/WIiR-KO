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


class Invoice(models.Model):
    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "06 - Faktury"
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
    information = models.TextField("Informacje", blank=True, null=True)
    creation_date = models.DateTimeField("Data utworzenia", auto_now_add=True)
    change_date = models.DateTimeField("Zmiana", auto_now=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name=related_name)
    slug = models.SlugField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.no_invoice} z dnia {self.date.strftime('%d.%m.%Y')} r."


# class InvoiceItems(models.Model):
#     class Meta:
#         verbose_name = "Element faktury"
#         verbose_name_plural = "Elementy faktury"
#         ordering = ["invoice_id"]
#
#     relatedName = "invoice_items"
#
#     invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name="Faktura",
#                                    related_name=relatedName)
#     account = models.ForeignKey(FinanceSource, on_delete=models.CASCADE, verbose_name="Konto",
#                                 related_name=relatedName)
#     unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="Jednostka",
#                              related_name=relatedName)
#     sum = models.DecimalField("Kwota brutto [zł]", max_digits=10, decimal_places=2, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.account} - {self.county} - {self.sum} zł."


# class CorrectiveNote(models.Model):
#     class Meta:
#         verbose_name = "Nota korygująca"
#         verbose_name_plural = "F.02 - Noty korygujące"
#         ordering = ["-date"]
#
#     relatedName = "correctivenote"
#
#     date = models.DateField("Data wystawienia")
#     no_note = models.CharField("Nr. noty", max_length=15)
#     contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name="Kontrahent",
#                                    related_name=relatedName)
#     corrective_invoice = models.CharField("Korygowana faktura", max_length=70)
#     information = models.TextField("Korygowana treść", blank=True, default="")
#     creation_date = models.DateField("Data uworzenia", auto_now_add=True)
#     author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Autor",
#                                related_name=relatedName)
#
#     def __str__(self):
#         return f"{self.no_note} z dnia {self.date}"


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


# class Source(models.Model):
#     class Meta:
#         verbose_name = "Źródło finansowania"
#         verbose_name_plural = "Źródła finansowania"
#
#     source = models.CharField("Źródło", max_length=80, null=True, unique=True)
#
#     def __str__(self):
#         return f"{self.source}"


class FinanceSource(models.Model):
    class Meta:
        verbose_name = "Konto"
        verbose_name_plural = "Konta"

    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Rozdział")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Grupa")
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, verbose_name="Paragraf")

    # source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name="Źródło finansowania")

    def __str__(self):
        return f"{self.section.section}-{self.group.group}-{self.paragraph}-{self.source}"
