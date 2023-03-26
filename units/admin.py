from django.contrib import admin
from units.models import County, TypeUnit, Unit


@admin.register(County)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'swop_id', 'id_order']


@admin.register(TypeUnit)
class TypeUnitAdmin(admin.ModelAdmin):
    list_display = ['type_short', 'type_full']


@admin.register(Unit)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['county_swop', 'type', 'city', 'manager', 'status']
