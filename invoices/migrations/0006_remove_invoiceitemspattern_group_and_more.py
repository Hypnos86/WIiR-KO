# Generated by Django 4.2.1 on 2023-09-14 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_section_swop_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitemspattern',
            name='group',
        ),
        migrations.RemoveField(
            model_name='invoiceitemspattern',
            name='invoice_id',
        ),
        migrations.RemoveField(
            model_name='invoiceitemspattern',
            name='paragraph',
        ),
        migrations.RemoveField(
            model_name='invoiceitemspattern',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='invoiceitemspattern',
            name='section',
        ),
        migrations.RemoveField(
            model_name='invoiceitemspattern',
            name='unit',
        ),
        migrations.DeleteModel(
            name='InvoiceItems',
        ),
        migrations.DeleteModel(
            name='InvoiceItemsPattern',
        ),
    ]