# Generated by Django 4.2.1 on 2023-09-14 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0005_remove_unit_cost_type_delete_costtype'),
        ('invoices', '0006_remove_invoiceitemspattern_group_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Kwota brutto [zł]')),
                ('information', models.CharField(max_length=400, verbose_name='Uwagi')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItemsP', to='invoices.group', verbose_name='Grupa')),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItemsP', to='invoices.invoice', verbose_name='Faktura')),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItemsP', to='invoices.paragraph', verbose_name='Paragraf')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItemsP', to='invoices.section', verbose_name='Rozdział')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItemsP', to='units.unit', verbose_name='Jednostka')),
            ],
            options={
                'ordering': ['invoice_id'],
            },
        ),
    ]
