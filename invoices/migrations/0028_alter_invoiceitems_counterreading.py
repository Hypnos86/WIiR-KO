# Generated by Django 4.2.1 on 2023-10-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0027_alter_invoiceitems_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitems',
            name='counterReading',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Stan licznika'),
        ),
    ]
