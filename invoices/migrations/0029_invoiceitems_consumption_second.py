# Generated by Django 4.2.1 on 2023-10-31 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0028_alter_invoiceitems_counterreading'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitems',
            name='consumption_second',
            field=models.IntegerField(blank=True, null=True, verbose_name='Zużycie-2'),
        ),
    ]