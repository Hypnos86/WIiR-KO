# Generated by Django 4.2.1 on 2023-09-14 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0005_remove_unit_cost_type_delete_costtype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoices', '0014_alter_invoiceitems_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitems',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data utworzenia'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='doc_types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='invoices.documenttypes', verbose_name='Rodzaj dokumentu'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='type_contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='invoices.contracttypes', verbose_name='Rodzaj umowy'),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItems', to='invoices.group', verbose_name='Grupa'),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='invoice_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItems', to='invoices.invoice', verbose_name='Faktura'),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='paragraph',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItems', to='invoices.paragraph', verbose_name='Paragraf'),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItems', to='invoices.section', verbose_name='Rozdział'),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItems', to='units.unit', verbose_name='Jednostka'),
        ),
    ]
