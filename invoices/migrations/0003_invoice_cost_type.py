# Generated by Django 4.1.7 on 2023-09-10 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_costtype_alter_documenttypes_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cost_type',
            field=models.ManyToManyField(related_name='invoice', to='invoices.costtype', verbose_name='Rodzaj kosztów'),
        ),
    ]
