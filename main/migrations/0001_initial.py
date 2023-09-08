# Generated by Django 4.1.7 on 2023-09-08 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountyCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True, verbose_name='Jednostka powiatowa')),
                ('id_order', models.IntegerField(null=True, unique=True, verbose_name='Kolejność')),
                ('slug', models.SlugField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Jednostka powiatowa',
                'verbose_name_plural': 'Jednostki powiatowe',
                'ordering': ['id_order'],
            },
        ),
        migrations.CreateModel(
            name='HelpInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information', models.TextField(verbose_name='Informacja')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Data dodania')),
                ('change', models.DateTimeField(auto_now=True, verbose_name='Zmiany')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_view', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Informacja',
                'verbose_name_plural': 'Informacje',
            },
        ),
    ]
