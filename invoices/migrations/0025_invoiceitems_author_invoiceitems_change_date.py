# Generated by Django 4.2.1 on 2023-09-21 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoices', '0024_alter_paragraph_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitems',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoiceitems',
            name='change_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Zmiana'),
        ),
    ]
