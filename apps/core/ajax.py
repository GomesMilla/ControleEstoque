from django.http import JsonResponse
from .models import Produto, Fornecedores, Marca, Tamanho, TipoProduto, Cliente, Produto

def fornecedor_por_empresa(request):
    empresa = request.user.empresa
    busca = request.GET.get('term', '')
    fornecedores = Fornecedores.objects.filter(empresa=empresa, nome__icontains=busca)
    resultados = [
        {'id': fornecedor.id, 'text': fornecedor.nome} for fornecedor in fornecedores
    ]
    return JsonResponse({'results': resultados})

def marca_por_empresa(request):
    empresa = request.user.empresa
    busca = request.GET.get('term', '')
    marcas = Marca.objects.filter(empresa=empresa, nome__icontains=busca)
    resultados = [
        {'id': marca.id, 'text': marca.nome} for marca in marcas
    ]
    return JsonResponse({'results': resultados})

def tamanho_por_empresa(request):
    empresa = request.user.empresa
    busca = request.GET.get('term', '')
    tamanhos = Marca.objects.filter(empresa=empresa, nome__icontains=busca)
    resultados = [
        {'id': tamanho.id, 'text': tamanho.nome} for tamanho in tamanhos
    ]
    return JsonResponse({'results': resultados})

def tipo_por_empresa(request):
    empresa = request.user.empresa
    busca = request.GET.get('term', '')
    tipos = TipoProduto.objects.filter(empresa=empresa, nome__icontains=busca)
    resultados = [
        {'id': tipo.id, 'text': tipo.nome} for tipo in tipos
    ]
    return JsonResponse({'results': resultados})

def produto_por_empresa(request):
    empresa = request.user.empresa
    busca = request.GET.get('term', '')
    produtos = Produto.objects.filter(empresa=empresa, nome__icontains=busca)
    resultados = [
        {'id': produto.id, 'text': produto.nome} for produto in produtos
    ]
    return JsonResponse({'results': resultados})

def cliente_por_empresa(request):
    empresa = request.user.empresa
    busca = request.GET.get('term', '')
    clientes = Cliente.objects.filter(empresa=empresa, nome__icontains=busca)
    resultados = [
        {'id': cliente.id, 'text': cliente.nome} for cliente in clientes
    ]
    return JsonResponse({'results': resultados})