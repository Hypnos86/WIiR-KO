# Generated by Django 4.2.7 on 2023-12-11 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('units', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='Typ dokumentu')),
            ],
            options={
                'verbose_name': 'Rodzaj umowy',
                'verbose_name_plural': '05 - Rodzaje umów',
            },
        ),
        migrations.CreateModel(
            name='DocumentTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='Typ dokumentu')),
            ],
            options={
                'verbose_name': 'Rodzaj dokumentu księgowego',
                'verbose_name_plural': '04 - Rodzaje dokumentów księgowych',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=2, unique=True, verbose_name='Grupa')),
                ('name', models.CharField(max_length=50, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Grupa',
                'verbose_name_plural': '02 - Grupy',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_receipt', models.DateField(verbose_name='Data wpływu')),
                ('date', models.DateField(verbose_name='Data wystawienia')),
                ('no_invoice', models.CharField(max_length=30, verbose_name='Nr. faktury')),
                ('sum', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Kwota [zł]')),
                ('date_of_payment', models.DateField(verbose_name='Termin płatności')),
                ('information', models.TextField(blank=True, null=True, verbose_name='Informacje')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('change_date', models.DateTimeField(auto_now=True, verbose_name='Zmiana')),
                ('slug', models.SlugField(blank=True, max_length=30, null=True, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('doc_types', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='invoices.documenttypes', verbose_name='Rodzaj dokumentu')),
            ],
            options={
                'verbose_name': 'Faktura',
                'verbose_name_plural': '07 - Faktury',
                'ordering': ['-date_receipt'],
            },
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragraph', models.CharField(max_length=7, unique=True, verbose_name='Paragraf')),
                ('name', models.CharField(max_length=100, verbose_name='Nazwa')),
                ('slug', models.SlugField(blank=True, max_length=7, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Paragraf i pozycja',
                'verbose_name_plural': '03 - Paragrafy i pozycje',
                'ordering': ['paragraph'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=5, unique=True, verbose_name='Rozdział')),
                ('name', models.CharField(max_length=20, verbose_name='Nazwa')),
                ('swop_id', models.ManyToManyField(blank=True, related_name='section', to='units.county', verbose_name='SWOP')),
            ],
            options={
                'verbose_name': 'Rozdział',
                'verbose_name_plural': '01 - Rozdziały',
                'ordering': ['section'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_from', models.DateField(verbose_name='Okres od')),
                ('period_to', models.DateField(verbose_name='Okres do')),
                ('measurementSystemNumber', models.CharField(blank=True, max_length=15, null=True, verbose_name='Nr. licznika')),
                ('counterReading', models.CharField(blank=True, max_length=80, null=True, verbose_name='Stan licznika')),
                ('consumption', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Zużycie')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Kwota brutto [zł]')),
                ('information', models.TextField(blank=True, null=True, verbose_name='Informacje')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('change_date', models.DateTimeField(auto_now=True, verbose_name='Zmiana')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('contract_types', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.contracttypes', verbose_name='Typ umowy')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoices.group', verbose_name='Grupa')),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoices.invoice', verbose_name='Faktura')),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoices.paragraph', verbose_name='Paragraf')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoices.section', verbose_name='Rozdział')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='units.unit', verbose_name='Jednostka')),
            ],
            options={
                'verbose_name': 'Element faktury',
                'verbose_name_plural': '06 - Elementy faktury',
                'ordering': ['-creation_date'],
            },
        ),
    ]
