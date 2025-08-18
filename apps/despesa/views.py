from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TipoDespesa, Despesa
from django.views.generic.edit import CreateView
from .forms import TipodeDespesaForm, DespesaForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView

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
