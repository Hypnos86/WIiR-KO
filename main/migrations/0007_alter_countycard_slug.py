<<<<<<< HEAD
# Generated by Django 4.1.7 on 2023-09-07 18:50
=======
# Generated by Django 4.2.1 on 2023-05-19 09:57
>>>>>>> 505266735d7ef6ac5b82a503df1e234adc1a536f

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_countycard_unit_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countycard',
            name='slug',
<<<<<<< HEAD
            field=models.SlugField(max_length=20, null=True),
=======
            field=models.SlugField(max_length=20, unique=True),
>>>>>>> 505266735d7ef6ac5b82a503df1e234adc1a536f
        ),
    ]
