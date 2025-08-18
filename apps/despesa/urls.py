from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .views import *

urlpatterns = [
    path('criar_tipo_despesa', TipodeDespesaCreateView.as_view(), name='criar_tipo_despesa'),
    path('listar_tipo_despesa', TiposdeDespesasListView.as_view(), name='listar_tipo_despesa'),

    path('criar_despesa', DespesaCreateView.as_view(), name='criar_despesa'),
    path('listar_despesa', DespesasMesList.as_view(), name='listar_despesa'),

]