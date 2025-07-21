from django.shortcuts import render
from .models import Evento
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from .forms import EventoForm
import calendar
from django.urls import reverse_lazy
from .models import Evento
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
from .models import Evento
from django.utils.timezone import now
import datetime
from django.views.generic.edit import UpdateView
from django.utils import timezone
from datetime import timedelta

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


PRIORIDADE_CORES = {
    'urgente':   {'background': '#dc3545', 'border': '#a71d2a'},  # vermelho
    'alta':      {'background': '#fd7e14', 'border': '#b85c0b'},  # laranja
    'media':     {'background': '#ffc107', 'border': '#b38600'},  # amarelo
    'baixa':     {'background': '#0d6efd', 'border': '#084298'},  # azul
}

def eventos_json(request):
    eventos_list = []
    ano_atual = timezone.now().year
    eventos = Evento.objects.filter(
        empresa=request.user.empresa,
        data_inicio__year=ano_atual
    )

    for evento in eventos:
        cor = PRIORIDADE_CORES.get(evento.prioridade, PRIORIDADE_CORES['baixa'])
        if evento.data_fim:
            end_date = evento.data_fim
        else:
            end_date = evento.data_inicio + timedelta(hours=1)
        # Evento de dia inteiro: começa e termina à meia-noite, e a diferença é >= 1 dia
        all_day = (
            evento.data_inicio.hour == 0 and evento.data_inicio.minute == 0 and evento.data_inicio.second == 0 and
            evento.data_fim and evento.data_fim.hour == 0 and evento.data_fim.minute == 0 and evento.data_fim.second == 0 and
            (evento.data_fim.date() - evento.data_inicio.date()).days >= 1
        )
        evento_dict = {
            'title': evento.titulo,
            'start': evento.data_inicio.isoformat(),
            'end': end_date.isoformat(),
            'description': evento.resumo,
            'tipo': evento.get_tipo_display(),
            'prioridade': evento.get_prioridade_display(),
            'recorrencia': evento.get_recorrencia_display() if evento.recorrencia else '',
            'backgroundColor': cor['background'],
            'borderColor': cor['border'],
            'textColor': '#fff',
        }
        if all_day:
            evento_dict['allDay'] = True
        # NÃO envie allDay para eventos com hora!
        eventos_list.append(evento_dict)
    return JsonResponse(eventos_list, safe=False)
