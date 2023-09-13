from django.contrib import admin
from units.models import County, TypeUnit, Unit


# @admin.register(CostType)
# class ContractorAdmin(admin.ModelAdmin):
#     list_display = ['name']


@admin.register(County)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'swop_id', 'id_order']


@admin.register(TypeUnit)
class TypeUnitAdmin(admin.ModelAdmin):
    list_display = ['type_short', 'id_order', 'type_full']


@admin.register(Unit)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['county_swop', 'type', 'address', 'city', 'manager', 'status']
    list_filter = ['county_swop']
    search_fields = ['address', 'city']
    search_help_text = "Szukaj po adresie lub mieście"
