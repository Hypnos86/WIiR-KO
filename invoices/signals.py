from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from invoices.models import Invoice, InvoiceItems, Paragraph, Section
from units.models import County


@receiver(post_save, sender=Invoice)
def createSlugInvoice(sender, instance, **kwargs):
    slug_text = f'{instance.no_invoice}-{instance.id}'
    if not instance.slug:
        instance.slug = slugify(slug_text, )
        instance.save()


@receiver(post_save, sender=Paragraph)
def createSlugParagraph(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.paragraph, )
        instance.save()


@receiver(post_save, sender=InvoiceItems)
def sumInvoiceItems(sender, instance, **kwargs):
    cost = []
    items = InvoiceItems.objects.filter(invoice_id=instance.invoice_id)

    for item in items:
        cost.append(item.sum)

    invoice = Invoice.objects.get(pk=instance.invoice_id.id)
    invoice.sum = sum(cost)
    invoice.save()


@receiver(post_delete, sender=InvoiceItems)
def sumInvoiceItems(sender, instance, **kwargs):
    cost = []
    items = InvoiceItems.objects.filter(invoice_id=instance.invoice_id)

    for item in items:
        cost.append(item.sum)

    invoice = Invoice.objects.get(pk=instance.invoice_id.id)
    invoice.sum = sum(cost)
    invoice.save()


@receiver(post_save, sender=InvoiceItems)
def addSectionToInvoiceItem(sender, instance, **kwargs):
    global section
    counties = County.objects.all()
    unit = instance.unit.county_swop.swop_id
    item = InvoiceItems.objects.get(pk=instance.id)

    for county in counties:
        if county.swop_id == unit:
            section = county.section.all().first()

    section = Section.objects.get(pk=section.id)
    item.section = section.id
    item.save()
