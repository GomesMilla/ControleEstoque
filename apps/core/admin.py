from django.contrib import admin
from .models import *

admin.site.register(Estoque)
admin.site.register(Produto)
admin.site.register(PeriodoMeta)
admin.site.register(Venda)
admin.site.register(Pedido)