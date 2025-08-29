from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TipoDespesa, Despesa
from django.views.generic.edit import CreateView
from .forms import TipodeDespesaForm, DespesaForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.db.models import Q
from django.db.models import Sum, F
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
class TipodeDespesaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TipoDespesa
    form_class = TipodeDespesaForm
    template_name = 'despesa/tipodespesa/criar.html'
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

class TiposdeDespesasListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = TipoDespesa
    template_name = 'despesa/tipodespesa/listar.html'
    context_object_name = 'tiposdedespesa'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TipoDespesa.objects.all()
        return TipoDespesa.objects.filter(empresa=self.request.user.empresa).order_by('-pk')[:10]

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class DespesaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesa/despesa/criar.html'
    success_url = reverse_lazy('listar_despesa')

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

class DespesaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Despesa
    form_class = DespesaForm
    template_name = 'despesa/despesa/editar.html'

    def get_success_url(self):
        return reverse_lazy('listar_despesa')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.empresa = self.request.user.empresa

            # COLOCANDO DATA DE PAGAMENTO DA DESPESA
            if form.instance.despesa_paga:
                form.instance.data_desativacao = datetime.now()

        return super().form_valid(form)

    def test_func(self):
        produto = self.get_object()
        return self.request.user.is_superuser or self.request.user.empresa is not None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class PagarDespesaView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        despesa = get_object_or_404(Despesa, pk=pk)

        if not self.test_func():
            return self.handle_no_permission()

        despesa.despesa_paga = True
        # COLOCANDO DATA DE PAGAMENTO DA DESPESA
        despesa.data_desativacao = datetime.now()
        despesa.save()
        return redirect(reverse_lazy('listar_despesa'))

    def test_func(self):
        # Opcional: ajuste a lógica conforme sua regra de acesso
        return self.request.user.is_superuser or self.request.user.empresa is not None

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class DespesasMesList(LoginRequiredMixin, ListView):
    model = Despesa
    template_name = 'despesa/despesa/listar.html'
    context_object_name = 'despesasmensais'

    def get_queryset(self):
        today = now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1))
        query = self.request.GET.get('q')

        if self.request.user.is_superuser:
            queryset = Despesa.objects.filter(data__range=(first_day_of_month, last_day_of_month))
        else:
            queryset = Despesa.objects.filter(
                empresa=self.request.user.empresa,
                data__range=(first_day_of_month, last_day_of_month)
            )

        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(resumo__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        despesas = self.get_queryset()

        total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or 0
        total_pagas = despesas.filter(despesa_paga=True).aggregate(total=Sum('valor'))['total'] or 0
        total_nao_pagas = despesas.filter(despesa_paga=False).aggregate(total=Sum('valor'))['total'] or 0

        context['total_despesas'] = total_despesas
        context['total_pagas'] = total_pagas
        context['total_nao_pagas'] = total_nao_pagas

        return context

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()