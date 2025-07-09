from django.contrib import admin
from .models import *
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'codigo', 'vendido')
    list_filter = ['empresa', 'vendido']
    search_fields = ['nome', 'codigo']

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'localizacao')
    list_filter = ['empresa']
    search_fields = ['nome']

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente_nome', 'empresa', 'cliente_telefone', 'vendedor', 'data_pedido')
    list_filter = ['status', 'empresa']
    search_fields = ['cliente_nome', 'vendedor']

class PeriodoMetaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'data_inicio', 'data_fim', 'fechado')
    list_filter = ['empresa', 'fechado', 'foi_lucro']
    search_fields = ['nome']

class VendaAdmin(admin.ModelAdmin):
    list_display = ('pk','vendedor', 'cliente', 'empresa', 'forma_pagamento', 'data_venda')
    list_filter = ['empresa', 'forma_pagamento', 'periodometa']
    search_fields = ['cliente', 'vendedor']

class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('pk','venda', 'venda_pk', 'produto', 'quantidade', 'empresa')
    list_filter = ['empresa', 'venda__periodometa']
    search_fields = ['produto', 'venda__cliente', 'venda__vendedor']

    def venda_pk(self, obj):
        return obj.venda.pk
    venda_pk.short_description = 'Venda PK'

class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'empresa')
    list_filter = ['empresa']
    search_fields = ['nome']

class TipoProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'empresa')
    list_filter = ['empresa']
    search_fields = ['nome']

admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(PeriodoMeta, PeriodoMetaAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Tamanho, TamanhoAdmin)
admin.site.register(TipoProduto, TipoProdutoAdmin)
admin.site.register(ContaCorrente)
admin.site.register(ItemVenda, ItemVendaAdmin)
admin.site.register(ValePresente)
