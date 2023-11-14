from django.contrib import admin
from main.models import CountyCard, HelpInfo

admin.site.site_title = "Admin WIiR-KO"
admin.site.index_title = "Administrator Kart Obiektów Wydziału Inwestycji i Remontów KWP w Poznaniu"


@admin.register(CountyCard)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id_order', 'slug']


@admin.register(HelpInfo)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['formatted_change', 'author']

    def formatted_change(self, obj):
        # Formatowanie daty w żądanym formacie
        return obj.change.strftime("%d-%m-%Y")  # Przykładowy format daty (RRRR-MM-DD GG:MM:SS)

    formatted_change.short_description = 'Change Date'
