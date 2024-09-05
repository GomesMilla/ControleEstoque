from django.urls import path
from django.views.generic import TemplateView
from .views import eventos_json, EventoCreateView, InicioView, EventosMesList, EventosAnualList, EventoUpdateViewView
from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    path("", InicioView.as_view(), name='agenda'),
    path('cadastrar_evento/', EventoCreateView.as_view(), name='cadastrar_evento'),
    path('editar_evento/<int:pk>/', EventoUpdateViewView.as_view(), name='editar_evento'),
    path('evento_mes/', EventosMesList.as_view(), name='evento_mes'),
    path('evento_anual/', EventosAnualList.as_view(), name='evento_anual'),
    path('events/json/', eventos_json, name='eventos_json'),
]