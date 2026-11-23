from django.contrib import admin
from .models import Calculation, MudProperty

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ('well_name', 'user', 'depth', 'density', 'ecd', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('well_name',)

@admin.register(MudProperty)
class MudPropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'density')

