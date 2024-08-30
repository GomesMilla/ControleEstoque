from django.contrib import admin
from .models import User, Empresa, Cliente

class UserAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'if_funcionario', 'is_active')
    list_filter = ['empresa']
    search_fields = ['nome']

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'genero', 'telefone_celular', 'data_aniversario')
    list_filter = ['empresa', 'genero']
    search_fields = ['nome']

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'razao_social', 'email')
    search_fields = ['nome', 'cnpj', 'razao_social']

admin.site.register(User, UserAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empresa, EmpresaAdmin)
