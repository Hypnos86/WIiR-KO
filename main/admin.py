from django.contrib import admin
from main.models import CountyCard, HelpInfo


# Register your models here.
@admin.register(CountyCard)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(HelpInfo)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['change', 'author']
