from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from datetime import date
from django.urls import reverse_lazy
from django.views.generic.edit import View
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum, F
from django.contrib import messages
from .forms import ItemVendaFormset
from django.views.generic.base import TemplateView

class EstoqueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Estoque
    form_class = EstoqueForm
    template_name = 'core/estoque/cadastrar_estoque.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class TamanhoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tamanho
    form_class = TamanhoForm
    template_name = 'core/tamanho/criar.html'
    success_url = reverse_lazy('listar_tamanho')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class TamanhoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tamanho
    template_name = 'core/tamanho/listar.html'
    context_object_name = 'tamanhos'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tamanho.objects.all()
        return Tamanho.objects.filter(empresa=self.request.user.empresa).order_by('-pk')[:10]

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class TipoProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TipoProduto
    form_class = TipoProdutoForm
    template_name = 'core/tipoproduto/criar.html'
    success_url = reverse_lazy('listar_tipos_de_produtos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class TipoProdutoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = TipoProduto
    template_name = 'core/tipoproduto/listar.html'
    context_object_name = 'tiposdeprodutos'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TipoProduto.objects.all()
        return TipoProduto.objects.filter(empresa=self.request.user.empresa).order_by('-pk')[:10]

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class MarcaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'core/marca/criar.html'
    success_url = reverse_lazy('listar_marcas')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class MarcaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Marca
    template_name = 'core/marca/listar.html'
    context_object_name = 'marcas'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Marca.objects.all()
        return Marca.objects.filter(empresa=self.request.user.empresa).order_by('-pk')[:10]

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class FornecedorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Fornecedores
    form_class = FornecedoresForm
    template_name = 'core/fornecedores/criar.html'
    success_url = reverse_lazy('listar_fornecedores')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class FornecedoresListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Fornecedores
    template_name = 'core/fornecedores/listar.html'
    context_object_name = 'fornecedores'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Fornecedores.objects.all()
        return Fornecedores.objects.filter(empresa=self.request.user.empresa).order_by('-pk')[:10]

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class DetalheFornecedorView(LoginRequiredMixin, DetailView):
    model = Fornecedores
    template_name = 'core/fornecedores/detalhe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objforncedor = Fornecedores.objects.get(pk=self.kwargs['pk'])
        produtos = Produto.objects.filter(empresa=self.request.user.empresa, fornecedor=objforncedor)

        context['objforncedor'] = objforncedor
        context['produtos'] = produtos
        return context

    def test_func(self):
        empresa = self.get_object()
        return self.request.user.is_superuser or (self.request.user.empresa == empresa and not self.request.user.if_funcionario)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class ProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'core/produto/cadastrar_produto.html'
    
    def get_success_url(self):
        return reverse_lazy('lista_produtos_empresa', kwargs={'pk': self.request.user.empresa.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.empresa is not None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class ProdutoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Produto
    template_name = 'core/produto/lista_produtos.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        empresa_pk = self.kwargs.get('pk')
        query = self.request.GET.get('q')

        if self.request.user.is_superuser and empresa_pk:
            empresa = get_object_or_404(Empresa, pk=empresa_pk)
            produtos = Produto.objects.filter(empresa=empresa)
        else:
            produtos = Produto.objects.filter(empresa=self.request.user.empresa, vendido=False)

        if query:
            produtos = produtos.filter(Q(nome__icontains=query) | Q(descricao__icontains=query) | Q(codigo__icontains=query) & Q(empresa=self.request.user.empresa))

        return produtos

    def test_func(self):
        empresa_pk = self.kwargs.get('pk')
        empresa = get_object_or_404(Empresa, pk=empresa_pk) if empresa_pk else None

        return self.request.user.is_superuser or self.request.user.empresa is not None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class ProdutoListIndisponivelView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Produto
    template_name = 'core/produto/produtoindisponivel.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        empresa_pk = self.kwargs.get('pk')
        query = self.request.GET.get('q')

        if self.request.user.is_superuser and empresa_pk:
            empresa = get_object_or_404(Empresa, pk=empresa_pk)
            produtos = Produto.objects.filter(empresa=empresa, vendido=True)
        else:
            produtos = Produto.objects.filter(empresa=self.request.user.empresa, vendido=True)

        if query:
            produtos = produtos.filter(Q(nome__icontains=query) | Q(descricao__icontains=query) | Q(codigo__icontains=query) & Q(empresa=self.request.user.empresa))

        return produtos

    def test_func(self):
        empresa_pk = self.kwargs.get('pk')
        empresa = get_object_or_404(Empresa, pk=empresa_pk) if empresa_pk else None

        return self.request.user.is_superuser or self.request.user.empresa is not None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class ProdutoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'core/produto/cadastrar_produto.html'

    def get_success_url(self):
        return reverse_lazy('lista_produtos_empresa', kwargs={'pk': self.request.user.empresa.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def test_func(self):
        produto = self.get_object()
        return self.request.user.is_superuser or self.request.user.empresa is not None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

# class ProdutoListView(ListView):
#     model = Produto
#     template_name = 'core/produto/loja.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         empresa_id = self.kwargs['empresa_id']
#         empresa = get_object_or_404(Empresa, id=empresa_id)
#         context['produtos_em_promocao'] = Produto.objects.filter(empresa=empresa, is_promocao=True, vendido=False)
#         context['produtos'] = Produto.objects.filter(empresa=empresa, vendido=False)
#         context['tipos_produto'] = TipoProduto.objects.filter(empresa=empresa)
#         context['tamanhos'] = Tamanho.objects.filter(empresa=empresa)
#         context['empresa'] = empresa

#         return context



class PeriodoMetaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PeriodoMeta
    form_class = PeriodoMetaForm
    template_name = 'core/meta/cadastrar_meta.html'
    success_url = reverse_lazy('lista_metas')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        if PeriodoMeta.objects.filter(empresa=form.instance.empresa, fechado=False).exists():
            form.add_error(None, "Já existe uma meta aberta para esta empresa.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or (self.request.user.empresa and not self.request.user.if_funcionario)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class FecharMetaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PeriodoMeta
    fields = ['data_fim']
    template_name = 'core/meta/fechar_meta.html'
    success_url = reverse_lazy('lista_metas')

    def form_valid(self, form):
        form.instance.fechado = True
        form.instance.data_fim = timezone.now()
        form.instance.valor_alcancado = form.instance.progresso()
        form.instance.foi_lucro = form.instance.valor_alcancado >= form.instance.valor_meta
        return super().form_valid(form)

    def test_func(self):
        meta = self.get_object()
        return self.request.user.is_superuser or (self.request.user.empresa == meta.empresa and not self.request.user.if_funcionario)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class PeriodoMetaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PeriodoMeta
    template_name = 'core/meta/lista_metas.html'
    context_object_name = 'metas'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PeriodoMeta.objects.all()
        return PeriodoMeta.objects.filter(empresa=self.request.user.empresa).order_by('-pk')[:10]

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class RelatorioMetaView(LoginRequiredMixin, DetailView):
    model = PeriodoMeta
    template_name = 'core/meta/relatorio.html'
    context_object_name = 'meta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = self.get_object()

        # Adiciona os dados do relatório no contexto
        context['relatorio'] = meta.relatorio_meta()
        return context

class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'core/pedido/cadastrar_pedido.html'
    success_url = reverse_lazy('lista_pedidos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        form.instance.empresa = self.request.user.empresa  # Define a empresa do pedido como a empresa do usuário logado
        # Garantir que o produto pertence à mesma empresa do vendedor
        if form.instance.produto and form.instance.produto.empresa != self.request.user.empresa:
            form.add_error('produto', 'O produto selecionado não pertence à sua empresa.')
            return self.form_invalid(form)
        return super().form_valid(form)

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'core/pedido/lista_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if self.request.user.is_superuser:
            queryset = Pedido.objects.all()
        else:
            queryset = Pedido.objects.filter(empresa=self.request.user.empresa, status='pendente')
        
        if query:
            queryset = queryset.filter(
                Q(cliente_nome__icontains=query) |
                Q(produto__nome__icontains=query) |
                Q(status__icontains=query) &
                Q(empresa=self.request.user.empresa)
            )
        
        return queryset
class PedidoListFiltroView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'core/pedido/lista_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        status = self.kwargs.get('status')  # Obtém o status da URL
        query = self.request.GET.get('q')

        # Se o usuário for superuser, mostra todos os pedidos
        if self.request.user.is_superuser:
            queryset = Pedido.objects.all()
        else:
            queryset = Pedido.objects.filter(empresa=self.request.user.empresa)

        # Aplica o filtro de status
        if status:
            queryset = queryset.filter(status=status)

        # Aplica o filtro de busca, se houver
        if query:
            queryset = queryset.filter(
                Q(cliente_nome__icontains=query) |
                Q(produto__nome__icontains=query) |
                Q(status__icontains=query) &
                Q(empresa=self.request.user.empresa)
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        # Garante que o contexto seja sempre passado, mesmo sem resultados no queryset
        context = super().get_context_data(**kwargs)
        context['status_atual'] = self.kwargs.get('status')  # Garante que o status atual seja enviado ao template
        context['termo_pesquisa'] = self.request.GET.get('q', '')  # Termo de pesquisa, padrão vazio se não houver
        return context


class PedidoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'core/pedido/cadastrar_pedido.html'
    success_url = reverse_lazy('lista_pedidos')

    def test_func(self):
        pedido = self.get_object()
        return self.request.user.is_superuser or self.request.user == pedido.vendedor or self.request.user.empresa == pedido.vendedor.empresa

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class VendaCreateView(LoginRequiredMixin, CreateView):
    model = Venda
    template_name = 'core/venda/cadastrar_venda.html'
    form_class = VendaForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['item_formset'] = ItemVendaFormset(user=self.request.user)
        else:
            data['item_formset'] = ItemVendaFormset(queryset=ItemVenda.objects.none(), user=self.request.user)
        return data

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        form.instance.empresa = self.request.user.empresa
        form.instance.periodometa = get_object_or_404(PeriodoMeta, fechado=False, empresa=self.request.user.empresa)
        self.object = form.save()
        from django.db import transaction
        with transaction.atomic():            
            item_formset = ItemVendaFormset(self.request.POST, instance=self.object, user=self.request.user)
            if item_formset.is_valid():
                itens = item_formset.save(commit=False)
                for item in itens:
                    produto = item.produto
                    quantidade = item.quantidade
                    if produto.quantidade < quantidade:
                        item_formset.add_error(None, f'Quantidade insuficiente no estoque para {produto.nome}.')
                        transaction.set_rollback(True)
                        return self.form_invalid(form)
                    produto.quantidade -= quantidade
                    if produto.quantidade <= 0:
                        produto.quantidade = 0
                        produto.vendido = True
                    produto.save()
                    item.empresa = self.request.user.empresa
                    item.save()
                item_formset.save_m2m()
                return super().form_valid(form)
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class VendaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Venda
    template_name = 'core/venda/lista_vendas.html'
    context_object_name = 'vendas'

    def get_queryset(self):
        periodometa_id = self.kwargs.get('periodometa_id')
        periodometa = get_object_or_404(PeriodoMeta, id=periodometa_id, empresa=self.request.user.empresa)
        return Venda.objects.filter(periodometa=periodometa, empresa=self.request.user.empresa).order_by('-pk')

    def test_func(self):
        return not self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodometa_id = self.kwargs.get('periodometa_id')
        context['periodometa'] = get_object_or_404(PeriodoMeta, id=periodometa_id, empresa=self.request.user.empresa)
        return context

class ValePresenteCreateView(LoginRequiredMixin, CreateView):
    model = ValePresente
    form_class = ValePresenteForm
    template_name = 'core/valepresente/cadastrar.html'
    success_url = reverse_lazy('listar_vale_presente')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        form.instance.empresa = self.request.user.empresa  # Define a empresa do pedido como a empresa do usuário logado
        # Garantir que o produto pertence à mesma empresa do vendedor
        return super().form_valid(form)

class ValePresenteList(LoginRequiredMixin, ListView):
    model = ValePresente
    template_name = 'core/valepresente/listar.html'
    context_object_name = 'vales'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if self.request.user.is_superuser:
            queryset = ValePresente.objects.all()
        else:
            queryset = ValePresente.objects.filter(empresa=self.request.user.empresa, status='pendente')
        
        if query:
            queryset = queryset.filter(
                Q(cliente_nome__icontains=query) |
                Q(cliente_ganhador_nome__icontains=query) &
                Q(empresa=self.request.user.empresa)
            )
        
        return queryset

class ValePresenteFiltroView(LoginRequiredMixin, ListView):
    model = ValePresente
    template_name = 'core/valepresente/listar.html'
    context_object_name = 'vales'

    def get_queryset(self):
        status = self.kwargs.get('status')  # Obtém o status da URL
        query = self.request.GET.get('q')

        # Se o usuário for superuser, mostra todos os pedidos
        if self.request.user.is_superuser:
            queryset = ValePresente.objects.all()
        else:
            queryset = ValePresente.objects.filter(empresa=self.request.user.empresa)

        # Aplica o filtro de status
        if status:
            queryset = queryset.filter(status=status)

        # Aplica o filtro de busca, se houver
        if query:
            queryset = queryset.filter(
                Q(cliente_nome__icontains=query) |
                Q(cliente__nome__icontains=query) |
                Q(cliente_ganhador_nome__icontains=query) |
                Q(cliente_ganhador__nome__icontains=query) |
                Q(status__icontains=query) &
                Q(empresa=self.request.user.empresa)
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        # Garante que o contexto seja sempre passado, mesmo sem resultados no queryset
        context = super().get_context_data(**kwargs)
        context['status_atual'] = self.kwargs.get('status')  # Garante que o status atual seja enviado ao template
        context['termo_pesquisa'] = self.request.GET.get('q', '')  # Termo de pesquisa, padrão vazio se não houver
        return context

class ValePresenteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ValePresente
    form_class = ValePresenteUpdateForm
    template_name = 'core/valepresente/editar.html'
    success_url = reverse_lazy('listar_vale_presente')

    def test_func(self):
        valepresente = self.get_object()
        return self.request.user.is_superuser or self.request.user == valepresente.vendedor or self.request.user.empresa == valepresente.vendedor.empresa

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class GenericDetailView(ListView):
    model = ValePresente 
    template_name = 'core/notificacao/notificacao.html'

    def get_context_data(self, **kwargs):
        from datetime import datetime, timedelta
        from django.utils import timezone
        data_de_hoje = timezone.now().date()
        today = timezone.now().date()
        context = super().get_context_data(**kwargs)

        inicio_do_dia = timezone.make_aware(datetime.combine(data_de_hoje, datetime.min.time()))
        fim_do_dia = timezone.make_aware(datetime.combine(data_de_hoje, datetime.max.time()))

        vales_presentes_vencendo = ValePresente.objects.filter(
            data_periodo_final__range=(inicio_do_dia, fim_do_dia), 
            empresa=self.request.user.empresa
        )
        
        aniversariantes = Cliente.objects.filter(
                    empresa=self.request.user.empresa,
                    data_aniversario__month=today.month,
                    data_aniversario__day=today.day)

        
        context["vales_presentes_vencendo"] = vales_presentes_vencendo
        context["aniversariantes"] = aniversariantes
        context["qtd_aniversariantes"] = aniversariantes.count()
        context["qtd_vales_presentes_vencendo"] = vales_presentes_vencendo.count()
        return context

class ContaCorrenteListView(LoginRequiredMixin,ListView):
    model = ContaCorrente
    template_name = 'core/contacorrente/listar.html'
    context_object_name = 'contas'

    def get_queryset(self):
        return ContaCorrente.objects.filter(empresa=self.request.user.empresa, is_active=True)

class ContaCorrenteCreateView(LoginRequiredMixin,CreateView):
    model = ContaCorrente
    form_class = ContaCorrenteForm
    template_name = 'core/contacorrente/criar.html'
    success_url = reverse_lazy('listar_contas')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ContaCorrenteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ContaCorrente
    form_class = ContaCorrenteForm
    template_name = 'core/contacorrente/editar.html'
    success_url = reverse_lazy('listar_contas')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        conta = self.get_object()
        return self.request.user.is_superuser or self.request.user.empresa == conta.empresa

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class ContaCorrenteInativarView(LoginRequiredMixin,View):
    model = ContaCorrente
    template_name = 'core/contacorrente/inativar.html'
    success_url = reverse_lazy('listar_contas')

    def get(self, request, *args, **kwargs):
        conta = self.get_object()
        return render(request, self.template_name, {'conta': conta})

    def post(self, request, *args, **kwargs):
        conta = self.get_object()
        conta.is_active = False  # Marcar como inativa
        conta.save()
        return redirect(self.success_url)

    def get_object(self):
        return ContaCorrente.objects.get(pk=self.kwargs['pk'], empresa=self.request.user.empresa)

class ContaCorrenteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ContaCorrente
    template_name = 'core/contacorrente/detalhe.html'
    context_object_name = 'conta'

    def test_func(self):
        # Verifica se o usuário pertence à mesma empresa da conta
        conta = self.get_object()
        return self.request.user.empresa == conta.empresa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conta = self.get_object()

        # Pegar todas as vendas fiado associadas à conta corrente
        vendas_fiado = conta.vendafiado_set.all()

        # Pegar os produtos comprados em cada venda fiado
        produtos_comprados = []
        for venda in vendas_fiado:
            itens_venda = venda.itens_venda.all()  # Pegando os produtos da venda
            for item in itens_venda:
                produtos_comprados.append({
                    'produto': item.produto.nome,
                    'quantidade': item.quantidade,
                    'preco_unitario': item.preco_unitario,
                    'total': item.quantidade * item.preco_unitario,
                    'venda_id': venda.id
                })

        context['vendas_fiado'] = vendas_fiado
        context['produtos_comprados'] = produtos_comprados
        return context


class VendaFiadoCreateView(LoginRequiredMixin, CreateView):
    model = VendaFiado
    form_class = VendaFiadoForm
    template_name = 'core/vendafiado/criar.html'
    success_url = reverse_lazy('listar_contas')

    def get_form_kwargs(self):
        """Passa o usuário autenticado para o formulário."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """Passa o formset e o usuário autenticado para o contexto."""
        data = super().get_context_data(**kwargs)

        if not hasattr(self.request.user, 'empresa'):
            raise ValueError("O usuário logado não tem uma empresa associada ou não está autenticado.")

        # Criando o formset para os itens de venda, passando o 'user' para o formset
        if self.request.POST:
            data['itens_form'] = ItemVendaFiadoFormset(self.request.POST, queryset=ItemVendaFiado.objects.none(), user=self.request.user)
        else:
            data['itens_form'] = ItemVendaFiadoFormset(queryset=ItemVendaFiado.objects.none(), user=self.request.user)

        return data

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        itens_form = context['itens_form']
        form.instance.empresa = self.request.user.empresa
        form.instance.periodometa = get_object_or_404(PeriodoMeta, fechado=False, empresa=self.request.user.empresa)
        form.instance.vendedor = self.request.user

        if itens_form.is_valid():
            total_venda = 0

            for item_form in itens_form.forms:
                if item_form.cleaned_data:
                    produto = item_form.cleaned_data['produto']
                    quantidade = item_form.cleaned_data['quantidade']

                    # Verificando se há estoque suficiente
                    if produto.quantidade < quantidade:
                        itens_form.add_error('quantidade', f"Estoque insuficiente para o produto {produto.nome}")
                        return self.form_invalid(form)

                    total_venda += produto.preco * quantidade
                    produto.quantidade -= quantidade
                    produto.save()

            form.instance.total = total_venda
            self.object = form.save()

            # Salvando os itens da venda
            for item_form in itens_form.forms:
                if item_form.cleaned_data:
                    ItemVendaFiado.objects.create(
                        venda=self.object,
                        produto=item_form.cleaned_data['produto'],
                        quantidade=item_form.cleaned_data['quantidade'],
                        preco_unitario=item_form.cleaned_data['produto'].preco,
                        empresa=self.request.user.empresa
                    )

            # Atualizando o saldo devedor da ContaCorrente
            conta_corrente = form.instance.conta_corrente
            conta_corrente.saldo_devedor += total_venda
            conta_corrente.save()

            # Gerar parcelas da venda fiado
            self.object.gerar_parcelas()
            return super().form_valid(form)

        return self.form_invalid(form)







class VendaFiadoListView(LoginRequiredMixin, ListView):
    model = VendaFiado
    template_name = 'core/vendafiado/listar.html'
    context_object_name = 'vendas'

    def get_queryset(self):
        # Obtém as vendas filtradas pela empresa do usuário logado
        return VendaFiado.objects.filter(empresa=self.request.user.empresa).prefetch_related('itens_venda', 'parcelas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obter o período meta atual (ajuste conforme sua lógica de meta)
        meta_atual = PeriodoMeta.objects.filter(empresa=self.request.user.empresa, fechado=False).first()

        if meta_atual:
            # Número de vendas em aberto da meta atual
            vendas_meta_abertas = VendaFiado.objects.filter(empresa=self.request.user.empresa, periodometa=meta_atual).exclude(parcelas__pendente=False).count()
            
            # Valor das contas fiado na meta atual
            total_fiado_meta = Parcela.objects.filter(venda__empresa=self.request.user.empresa, venda__periodometa=meta_atual, pendente=True).aggregate(total_fiado=Sum(F('valor')))['total_fiado'] or 0
            
            context['vendas_meta_abertas'] = vendas_meta_abertas
            context['total_fiado_meta'] = total_fiado_meta
        else:
            context['vendas_meta_abertas'] = 0
            context['total_fiado_meta'] = 0

        # Total a receber (de todas as metas)
        total_a_receber = Parcela.objects.filter(venda__empresa=self.request.user.empresa, pendente=True).aggregate(total_receber=Sum(F('valor')))['total_receber'] or 0
        context['total_a_receber'] = total_a_receber

        # Calcula se cada venda está paga ou não
        vendas = context['vendas']
        for venda in vendas:
            if venda.parcelas.filter(pendente=True).exists():
                venda.status = "Pendente"
            else:
                venda.status = "Pago"

        return context

class VendaFiadoDetailView(LoginRequiredMixin, DetailView):
    model = VendaFiado
    template_name = 'core/vendafiado/view.html'
    context_object_name = 'venda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venda = self.get_object()

        # Obtém as parcelas relacionadas à venda
        context['parcelas'] = venda.parcelas.all()

        return context

class PagarParcelaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Parcela
    fields = []  # Não exibe nenhum campo, já que o pagamento é automático
    template_name = 'core/vendafiado/pagar.html'
    success_url = reverse_lazy('listar_vendas_fiado')

    def test_func(self):
        # Garantir que o usuário faz parte da empresa da parcela
        parcela = self.get_object()
        return self.request.user.empresa == parcela.empresa

    def form_valid(self, form):
        parcela = form.save(commit=False)
        parcela.pendente = False  # Marca a parcela como paga
        parcela.vendedor = self.request.user  # Define o usuário logado como o vendedor
        parcela.data_atualizacao = timezone.now()  # Define a data do pagamento
        parcela.save()

        # Atualiza o saldo devedor na conta corrente associada à venda
        conta_corrente = parcela.venda.conta_corrente
        conta_corrente.saldo_devedor -= parcela.valor
        conta_corrente.save()

        # Exibe uma mensagem de sucesso
        messages.success(self.request, 'Pagamento da parcela realizado com sucesso.')

        # Redireciona para os detalhes da venda
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona para os detalhes da venda após o pagamento
        return reverse_lazy('detalhar_venda_fiado', kwargs={'pk': self.object.venda.pk})

class RelatoriosView(LoginRequiredMixin, TemplateView):
    template_name = 'core/relatorios/home.html'