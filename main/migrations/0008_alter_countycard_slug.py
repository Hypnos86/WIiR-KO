# Generated by Django 4.2.1 on 2023-05-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_countycard_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countycard',
            name='slug',
            field=models.SlugField(max_length=20, null=True, unique=True),
        ),
    ]
