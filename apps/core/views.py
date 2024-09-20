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
from datetime import date

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['item_form'] = ItemVendaForm(self.request.POST, user=self.request.user)
        else:
            data['item_form'] = ItemVendaForm(user=self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        item_form = context['item_form']
        form.instance.vendedor = self.request.user
        form.instance.empresa = self.request.user.empresa
        form.instance.periodometa = get_object_or_404(PeriodoMeta, fechado=False, empresa=self.request.user.empresa)

        if item_form.is_valid():
            produto = item_form.cleaned_data['produto']
            quantidade = item_form.cleaned_data['quantidade']

            print(f"Produto: {produto.nome}, Quantidade no estoque: {produto.quantidade}, Quantidade solicitada: {quantidade}")

            if produto.quantidade < quantidade:
                item_form.add_error('quantidade', 'Quantidade insuficiente no estoque.')
                return self.form_invalid(form)

            from django.db import transaction
            with transaction.atomic():
                # Atualizar a quantidade do produto e o status antes de salvar
                produto.quantidade -= quantidade
                if produto.quantidade <= 0:
                    produto.quantidade = 0
                    produto.vendido = True
                produto.save()

                print(f"Produto após atualização: {produto.nome}, Quantidade restante no estoque: {produto.quantidade}, Vendido: {produto.vendido}")

                # Salvar a venda
                self.object = form.save()

                # Criar o item da venda
                item = item_form.save(commit=False)
                item.venda = self.object
                item.empresa = self.request.user.empresa
                item.save()

                print(f"Produto após item salvo: {produto.nome}, Quantidade restante no estoque: {produto.quantidade}, Vendido: {produto.vendido}")

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
        return Venda.objects.filter(periodometa=periodometa, empresa=self.request.user.empresa)

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
