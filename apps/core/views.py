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

class ProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'core/produto/cadastrar_produto.html'
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
            produtos = produtos.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))

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
            produtos = produtos.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))

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
        elif self.request.user.if_funcionario:
            queryset = Pedido.objects.filter(vendedor=self.request.user)
        else:
            queryset = Pedido.objects.filter(vendedor__empresa=self.request.user.empresa)
        
        if query:
            queryset = queryset.filter(
                Q(cliente_nome__icontains=query) |
                Q(produto__nome__icontains=query) |
                Q(status__icontains=query)
            )
        
        return queryset

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