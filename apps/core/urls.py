from django.urls import path
from .views import *
from .ajax import *

urlpatterns = [
    # estoque
    path('cadastrar_estoque/', EstoqueCreateView.as_view(), name='cadastrar_estoque'),

    #tamanho
    path('cadastrar_tamanho/', TamanhoCreateView.as_view(), name='cadastrar_tamanho'),
    path('listar_tamanho/', TamanhoListView.as_view(), name='listar_tamanho'),

    #tipo produto
    path('cadastrar_tipo_produto/', TipoProdutoCreateView.as_view(), name='tipo_produto_criar'),
    path('listar_tipo/', TipoProdutoListView.as_view(), name='listar_tipos_de_produtos'),

    #marca
    path('cadastrar_marca/', MarcaCreateView.as_view(), name='cadastrar_marca'),
    path('listar_marcas/', MarcaListView.as_view(), name='listar_marcas'),

    #fornecedores
    path('cadastrar_fornecedores/', FornecedorCreateView.as_view(), name='cadastrar_fornecedor'),
    path('listar_fornecedores/', FornecedoresListView.as_view(), name='listar_fornecedores'),
    path('detalhes_fornecedor/<int:pk>/', DetalheFornecedorView.as_view(), name='detalhes_fornecedor'),
    
    # produto
    path('cadastrar_produto/', ProdutoCreateView.as_view(), name='cadastrar_produto'),
    path('lista_produtos/<int:pk>/', ProdutoListView.as_view(), name='lista_produtos_empresa'),
    path('lista_produtos_indisponivel/<int:pk>/', ProdutoListIndisponivelView.as_view(), name='lista_produtos_indisponivel'),
    path('editar_produto/<int:pk>/', ProdutoUpdateView.as_view(), name='editar_produto'),
    path('loja/<int:empresa_id>/produtos/', ProdutoListView.as_view(), name='loja'),


    # meta
    path('cadastrar_meta/', PeriodoMetaCreateView.as_view(), name='cadastrar_meta'),
    path('fechar_meta/<int:pk>/', FecharMetaView.as_view(), name='fechar_meta'),
    path('lista_metas/', PeriodoMetaListView.as_view(), name='lista_metas'),
    path('vendas/meta/<int:periodometa_id>/', VendaListView.as_view(), name='lista_vendas_meta'),
    path('meta/relatorio/<int:pk>/', RelatorioMetaView.as_view(), name='relatorio_meta'),

    #pedido
    path('cadastrar_pedido/', PedidoCreateView.as_view(), name='cadastrar_pedido'),
    path('lista_pedidos/', PedidoListView.as_view(), name='lista_pedidos'),
    path('atualizar_pedido/<int:pk>/', PedidoUpdateView.as_view(), name='atualizar_pedido'),
    path('pedidos/<str:status>/', PedidoListFiltroView.as_view(), name='filtrar_pedidos'),

    # venda
    path('cadastrar_venda/', VendaCreateView.as_view(), name='cadastrar_venda'),
    

    # Vale Presente
    path('cadastrar_vale_presente/', ValePresenteCreateView.as_view(), name='cadastrar_vale_presente'),
    path('listar_vale_presente/', ValePresenteList.as_view(), name='listar_vale_presente'),
    path('editar_pedido/<int:pk>/', ValePresenteUpdateView.as_view(), name='editar_pedido'),
    path('valepresente/<str:status>/', ValePresenteFiltroView.as_view(), name='filtrar_valespresente'),

    #Notificações
    path('pendencias/', GenericDetailView.as_view(), name='pendencias'),

    # Conta Corrente
    path('conta_corrente/nova/', ContaCorrenteCreateView.as_view(), name='nova_conta'),
    path('conta_corrente/editar/<int:pk>/', ContaCorrenteUpdateView.as_view(), name='editar_conta'),
    path('conta_corrente/inativar/<int:pk>/', ContaCorrenteInativarView.as_view(), name='inativar_conta'),
    path('conta_corrente/', ContaCorrenteListView.as_view(), name='listar_contas'),
    path('conta/<int:pk>/', ContaCorrenteDetailView.as_view(), name='detalhar_conta_corrente'),

    # Venda a Prazo
    path('venda-fiado/nova/', VendaFiadoCreateView.as_view(), name='nova_venda_fiado'),
    path('vendas-fiado/', VendaFiadoListView.as_view(), name='listar_vendas_fiado'),
    path('vendas-fiado/<int:pk>/', VendaFiadoDetailView.as_view(), name='detalhar_venda_fiado'),
    path('vendas-fiado/parcela/pagar/<int:pk>/', PagarParcelaView.as_view(), name='pagar_parcela'),

    #AJAX
    path('fornecedores_pesquisar/', fornecedor_por_empresa, name='fornecedores_pesquisar'),
    path('marca_pesquisar/', marca_por_empresa, name='marca_pesquisar'),
    path('tamanho_pesquisar/', tamanho_por_empresa, name='tamanho_pesquisar'),
    path('tipos_pesquisar/', tipo_por_empresa, name='tipos_pesquisar'),
    path('cliente_pesquisar/', cliente_por_empresa, name='cliente_pesquisar'),
    path('produto_pesquisar/', produto_por_empresa, name='produto_pesquisar'),
]