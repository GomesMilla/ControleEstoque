from django.shortcuts import render
from .models import Evento
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from .forms import EventoForm
import calendar
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.utils.timezone import now
import datetime
from django.views.generic.edit import UpdateView
from django.utils import timezone
from datetime import timedelta
from users.models import Cliente

class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "agenda/inicio.html"
    login_url = '/login/'

class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'agenda/cadastrar.html'
    success_url = reverse_lazy('agenda')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.user = self.request.user
            form.instance.empresa = self.request.user.empresa 
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class EventoUpdateViewView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'agenda/editar.html'
    success_url = reverse_lazy('agenda')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.user = self.request.user
            form.instance.empresa = self.request.user.empresa 
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.if_funcionario or self.request.user.if_funcionario

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()

class EventosMesList(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'agenda/listar.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        today = now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (today.replace(month=today.month % 12 + 1, day=1) - datetime.timedelta(days=1))
        query = self.request.GET.get('q')

        if self.request.user.is_superuser:
            queryset = Evento.objects.all()

        else:
            queryset = Evento.objects.filter(
            empresa=self.request.user.empresa,
            data_inicio__gte=first_day_of_month,
            data_fim__lte=last_day_of_month
        )        
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(resumo__icontains=query) |
                Q(empresa=self.request.user.empresa) |
                Q(data_inicio__gte=first_day_of_month) |
                Q(data_fim__lte=last_day_of_month)
            )
        
        return queryset

class EventosAnualList(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'agenda/listar.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        today = now().date()
        first_day_of_year = today.replace(month=1, day=1)
        last_day_of_year = today.replace(month=12, day=31)
        current_year = today.year
        query = self.request.GET.get('q')

        if self.request.user.is_superuser:
            queryset = Evento.objects.all()
        else:
            queryset = Evento.objects.filter(
                empresa=self.request.user.empresa,
                data_inicio__year=current_year,
                data_inicio__gte=first_day_of_year,
                data_fim__lte=last_day_of_year
            )

        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(resumo__icontains=query) |
                Q(empresa=self.request.user.empresa) |
                Q(data_inicio__gte=first_day_of_year) |
                Q(data_fim__lte=last_day_of_year)
            )
        
        return queryset


def eventos_json(request):
    eventos_list = []
    
    # Obter parâmetros de data da requisição
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    if start_date and end_date:
        # Converter strings para objetos datetime
        from datetime import datetime
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Buscar eventos no período
        eventos = Evento.objects.filter(
            empresa=request.user.empresa,
            data_inicio__gte=start_dt.date(),
            data_fim__lte=end_dt.date()
        )
        
        # Adicionar eventos à lista
        for evento in eventos:
            end_date_event = evento.data_fim + timedelta(days=1) if evento.data_fim else None
            eventos_list.append({
                'title': evento.titulo,
                'start': evento.data_inicio.isoformat(),
                'end': end_date_event.isoformat() if end_date_event else None,
                'description': evento.resumo,
                'type': 'evento',
                'backgroundColor': '#007bff',  # Azul para eventos
                'borderColor': '#0056b3'
            })
        
        # Buscar aniversariantes no período
        # Para aniversários, precisamos verificar se a data de aniversário cai no período
        # Vamos buscar todos os clientes e verificar se o aniversário cai no período
        aniversariantes = Cliente.objects.filter(
            empresa=request.user.empresa
        )
        
        for cliente in aniversariantes:
            # Criar data de aniversário para o ano atual
            ano_atual = timezone.now().year
            data_aniversario = cliente.data_aniversario.replace(year=ano_atual)
            
            # Verificar se o aniversário cai no período selecionado
            if start_dt.date() <= data_aniversario <= end_dt.date():
                eventos_list.append({
                    'title': f"Aniversário: {cliente.nome}",
                    'start': data_aniversario.isoformat(),
                    'end': (data_aniversario + timedelta(days=1)).isoformat(),
                    'description': f"Aniversário de {cliente.nome}",
                    'type': 'aniversario',
                    'backgroundColor': '#28a745',  # Verde para aniversários
                    'borderColor': '#1e7e34'
                })
    else:
        # Fallback: buscar eventos do ano atual (comportamento anterior)
        ano_atual = timezone.now().year 
        eventos = Evento.objects.filter(
            empresa=request.user.empresa,
            data_inicio__year=ano_atual
        )
        
        # Adicionar eventos à lista
        for evento in eventos:
            end_date = evento.data_fim + timedelta(days=1) if evento.data_fim else None
            eventos_list.append({
                'title': evento.titulo,
                'start': evento.data_inicio.isoformat(),
                'end': end_date.isoformat() if end_date else None,
                'description': evento.resumo,
                'type': 'evento',
                'backgroundColor': '#007bff',  # Azul para eventos
                'borderColor': '#0056b3'
            })
        
        # Buscar aniversariantes do ano atual
        aniversariantes = Cliente.objects.filter(
            empresa=request.user.empresa
        )
        
        # Adicionar aniversariantes à lista
        for cliente in aniversariantes:
            # Criar data de aniversário para o ano atual
            data_aniversario = cliente.data_aniversario.replace(year=ano_atual)
            
            eventos_list.append({
                'title': f"Aniversário: {cliente.nome}",
                'start': data_aniversario.isoformat(),
                'end': (data_aniversario + timedelta(days=1)).isoformat(),
                'description': f"Aniversário de {cliente.nome}",
                'type': 'aniversario',
                'backgroundColor': '#28a745',  # Verde para aniversários
                'borderColor': '#1e7e34'
            })
    
    return JsonResponse(eventos_list, safe=False)
