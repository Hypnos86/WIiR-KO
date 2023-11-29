from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportMixin

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


class CountyResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Identyfikator')
    county_unit = Field(attribute='county_unit', column_name='Powiat')
    county_swop = Field(attribute='county_swop', column_name='SWOP')
    type = Field(attribute='type', column_name='Rodzaj jednostki')
    address = Field(attribute='address', column_name='Adres')
    zip_code = Field(attribute='zip_code', column_name='Kod pocztowy')
    city = Field(attribute='city', column_name='Miasto')
    object_name = Field(attribute='object_name', column_name='Obiekt')
    manager = Field(attribute='manager', column_name='Administrator')
    status = Field(attribute='status', column_name='Status')
    information = Field(attribute='information', column_name='Informacje')

    class Meta:
        model = Unit
        fields = (
            'id', 'county_unit', 'county_swop', 'type', 'address', 'zip_code', 'city', 'object_name', 'manager',
            'status', 'information')

        export_order = (
            'id', 'county_unit', 'county_swop', 'type', 'address', 'zip_code', 'city', 'object_name', 'manager',
            'status', 'information')


@admin.register(Unit)
class ContractorAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['county_swop', 'type', 'address', 'city', 'manager', 'status']
    list_filter = ['county_swop']
    search_fields = ['address', 'city']
    search_help_text = "Szukaj po adresie lub mieście"
    resource_class = CountyResource
