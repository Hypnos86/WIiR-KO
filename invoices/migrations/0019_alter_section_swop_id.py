# Generated by Django 4.2.1 on 2023-09-19 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0005_remove_unit_cost_type_delete_costtype'),
        ('invoices', '0018_alter_section_swop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='swop_id',
            field=models.ManyToManyField(blank=True, null=True, related_name='section', to='units.county', verbose_name='SWOP'),
        ),
    ]