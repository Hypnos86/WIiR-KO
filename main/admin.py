from django.contrib import admin
from main.models import CountyCard, HelpInfo

admin.site.site_title = "Admin WIiR-APP"
admin.site.index_title = "Administrator Kart Obiektów Wydziału Inwestycji i Remontów KWP w Poznaniu"


@admin.register(CountyCard)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(HelpInfo)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['change', 'author']
