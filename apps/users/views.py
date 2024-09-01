from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .models import Empresa, User, Cliente
from .forms import EmpresaForm, UserForm, UserFormAdmin, ClienteForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from core.models import PeriodoMeta, Venda
from django.db.models import Q
from django.views import View
from datetime import date

def base(request):
    context = {
        'now' : timezone.now().time(),
    }
    area_url = request.META.get('PATH_INFO')
    if request.user.is_authenticated and not "/admin/" in area_url:
        objeuser = request.user
        context = {
            'now': timezone.now().time(),
            "objuser" : objeuser,
        }
    
    return context

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'users/users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        empresa = user.empresa
        data_de_hoje = date.today()
        # Informações da meta para a dona da empresa
        if not user.if_funcionario:
            meta_atual = PeriodoMeta.objects.filter(empresa=empresa, fechado=False).first()
            if meta_atual:
                context['meta_atual'] = meta_atual
                context['valor_meta'] = meta_atual.valor_meta
                context['valor_alcancado'] = meta_atual.progresso()
                context['falta_para_meta'] = meta_atual.falta_para_meta()
                context['ultimas_vendas'] = Venda.objects.filter(empresa=empresa, data_venda__date=data_de_hoje).order_by('-data_venda')
                context['objuser'] = self.request.user
                context['data_atual'] = data_de_hoje
        else:
            # Informações para funcionários
            context['ultimas_vendas'] = Venda.objects.filter(vendedor=user, data_venda__date=data_de_hoje).order_by('-data_venda')

        return context

class EmpresaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'users/empresa/criar_empresa.html'
    success_url = reverse_lazy('lista_empresas')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class EmpresaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Empresa
    template_name = 'users/empresa/lista_empresas.html'
    context_object_name = 'empresas'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')  # Redireciona para uma página padrão se não for superadmin
        return super().handle_no_permission()


class EmpresaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'users/empresa/editar_empresa.html'
    success_url = reverse_lazy('lista_empresas')

    def test_func(self):
        return self.request.user.is_superuser or (not self.request.user.if_funcionario and self.request.user.empresa == self.get_object())

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class InativarEmpresaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Empresa
    fields = []
    template_name = 'users/empresa/inativar_empresa.html'
    success_url = reverse_lazy('lista_empresas')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        empresa = self.get_object()
        empresa.ativo = False
        empresa.save()
        
        # Desativar todos os usuários da empresa
        User.objects.filter(empresa=empresa).update(is_active=False)
        
        messages.success(request, f'A empresa {empresa.nome} foi inativada com sucesso.')
        return redirect(self.success_url)

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/users/cadastrar_usuario.html'

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lista_usuarios', kwargs={'pk': self.request.user.empresa.pk})

    def test_func(self):
        return not self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/users/editar_usuario.html'

    def get_success_url(self):
        return reverse_lazy('lista_usuarios', kwargs={'pk': self.request.user.empresa.pk})

    def test_func(self):
        user = self.get_object()
        return self.request.user.is_superuser or self.request.user == user or (
            not self.request.user.if_funcionario and self.request.user.empresa == user.empresa
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class UserDeactivateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return not self.request.user.if_funcionario and self.request.user.empresa == user.empresa

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        if self.test_func():
            if user != request.user:  # Verifica para evitar desativar o próprio usuário
                user.is_active = False
                user.excluido = False  # Assegura que não seja excluído, apenas inativado
                user.save()
        return redirect('lista_usuarios', pk=self.request.user.empresa.pk)

class UserCreateViewAdmin(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserFormAdmin
    template_name = 'users/users/cadastrar_usuario.html'
    success_url = reverse_lazy('lista_empresas')

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('lista_empresas')
        return super().handle_no_permission()

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/users/lista_usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        empresa_pk = self.kwargs.get('pk')
        empresa = get_object_or_404(Empresa, pk=empresa_pk)

        if self.request.user.is_superuser:
            return User.objects.filter(empresa=empresa)
        
        if self.request.user.empresa == empresa and not self.request.user.if_funcionario:
            return User.objects.filter(empresa=empresa)

        return User.objects.none()

    def test_func(self):
        empresa_pk = self.kwargs.get('pk')
        empresa = get_object_or_404(Empresa, pk=empresa_pk)
        return self.request.user.is_superuser or (self.request.user.empresa == empresa and not self.request.user.if_funcionario)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class EmpresaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Empresa
    template_name = 'users/empresa/detalhes_empresa.html'
    context_object_name = 'empresa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcionarios'] = User.objects.filter(empresa=self.get_object())
        return context

    def test_func(self):
        empresa = self.get_object()
        return self.request.user.is_superuser or (self.request.user.empresa == empresa and not self.request.user.if_funcionario)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'users/cliente/cadastrar_cliente.html'
    success_url = reverse_lazy('lista_clientes')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'users/cliente/cadastrar_cliente.html'
    success_url = reverse_lazy('lista_clientes')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'users/cliente/lista_clientes.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Cliente.objects.filter(empresa=self.request.user.empresa)
        
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(telefone_celular__icontains=query) |
                Q(cpf__icontains=query)
            )
        
        return queryset

class DetalheCliente(LoginRequiredMixin, DetailView):
    model = Empresa
    template_name = 'users/cliente/detalhe_cliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objcliente = Cliente.objects.get(pk=self.kwargs['pk'])
        compras_cliente = Venda.objects.filter(empresa=self.request.user.empresa, cliente=objcliente)

        context['objcliente'] = objcliente
        context['compras_cliente'] = compras_cliente
        return context

    def test_func(self):
        empresa = self.get_object()
        return self.request.user.is_superuser or (self.request.user.empresa == empresa and not self.request.user.if_funcionario)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()


class AniversariantesListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'users/cliente/aniversariantes.html'
    context_object_name = 'aniversariantes'

    def get_queryset(self):
        today = timezone.now().date()
        return Cliente.objects.filter(
            empresa=self.request.user.empresa,
            data_aniversario__month=today.month,
            data_aniversario__day=today.day
        )