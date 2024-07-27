from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    
    # empresa
    path('cadastrar_empresa/', EmpresaCreateView.as_view(), name='cadastrar_empresa'),
    path('lista_empresas/', EmpresaListView.as_view(), name='lista_empresas'),
    path('editar_empresa/<int:pk>/', EmpresaUpdateView.as_view(), name='editar_empresa'),
    path('inativar_empresa/<int:pk>/', InativarEmpresaView.as_view(), name='inativar_empresa'),
    path('detalhes_empresa/<int:pk>/', EmpresaDetailView.as_view(), name='detalhes_empresa'),
    
    # usuario
    path('cadastrar_usuario/', UserCreateView.as_view(), name='cadastrar_usuario'),
    path('cadastrar_usuario_admin/', UserCreateViewAdmin.as_view(), name='cadastrar_usuario_admin'),
    path('lista_usuarios/<int:pk>/', UserListView.as_view(), name='lista_usuarios'),
    path('editar_usuario/<int:pk>/', UserUpdateView.as_view(), name='editar_usuario'),
    path('inativar_usuario/<int:pk>/', UserDeactivateView.as_view(), name='inativar_usuario'),

    # clientes
    path('cadastrar_cliente/', ClienteCreateView.as_view(), name='cadastrar_cliente'),
    path('editar_cliente/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('lista_clientes/', ClienteListView.as_view(), name='lista_clientes'),
    path('aniversariantes/', AniversariantesListView.as_view(), name='aniversariantes'),
]