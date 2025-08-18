from django.contrib import admin
from .models import TipoDespesa, Despesa

@admin.register(TipoDespesa)
class TipoDespesaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('titulo','descricao', 'valor', 'data', 'tipo', 'eh_extra')
    list_filter = ('tipo', 'eh_extra', 'data')
    search_fields = ('descricao',)
