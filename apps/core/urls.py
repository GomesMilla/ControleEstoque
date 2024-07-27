from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar_estoque/', EstoqueCreateView.as_view(), name='cadastrar_estoque'),
    
    # produto
    path('cadastrar_produto/', ProdutoCreateView.as_view(), name='cadastrar_produto'),
    path('lista_produtos/<int:pk>/', ProdutoListView.as_view(), name='lista_produtos_empresa'),
    path('lista_produtos_indisponivel/<int:pk>/', ProdutoListIndisponivelView.as_view(), name='lista_produtos_indisponivel'),
    path('editar_produto/<int:pk>/', ProdutoUpdateView.as_view(), name='editar_produto'),

    # meta
    path('cadastrar_meta/', PeriodoMetaCreateView.as_view(), name='cadastrar_meta'),
    path('fechar_meta/<int:pk>/', FecharMetaView.as_view(), name='fechar_meta'),
    path('lista_metas/', PeriodoMetaListView.as_view(), name='lista_metas'),
    path('vendas/meta/<int:periodometa_id>/', VendaListView.as_view(), name='lista_vendas_meta'),

    #pedido
    path('cadastrar_pedido/', PedidoCreateView.as_view(), name='cadastrar_pedido'),
    path('lista_pedidos/', PedidoListView.as_view(), name='lista_pedidos'),
    path('atualizar_pedido/<int:pk>/', PedidoUpdateView.as_view(), name='atualizar_pedido'),

    # venda
    path('cadastrar_venda/', VendaCreateView.as_view(), name='cadastrar_venda'),
]