# Generated by Django 4.1.7 on 2023-09-07 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0008_alter_unit_county_swop_alter_unit_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
