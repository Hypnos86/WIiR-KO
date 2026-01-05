from django.contrib import admin
from cpvdict.models import Genre, Typecpv, OrderLimit

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name_id', 'name']
    search_fields = ['name_id', 'name']
    filter_horizontal = ['cpv']
    
@admin.register(OrderLimit)
class OrderLimitAdmin(admin.ModelAdmin):
    list_display = ['year','euro_exchange_rate', 'limit_euro', 'limit_netto' ]   

@admin.register(Typecpv)
class TypecpvAdmin(admin.ModelAdmin):
    list_display = ['no_cpv', 'name']
    search_fields = ['no_cpv', 'name']