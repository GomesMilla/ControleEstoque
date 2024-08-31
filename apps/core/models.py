from django.db import models
from users.models import User, Empresa, BaseModel, Cliente
import random
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class Estoque(BaseModel):
    nome = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='estoques')
    localizacao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Produto(BaseModel):
    nome = models.CharField(max_length=255)
    descricao = RichTextUploadingField("Descrição do produto:")
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produtos')
    imagemperfil = models.ImageField("Foto de Produto", upload_to="fotoproduto/", null=True, blank=True)
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='produto_estoque')
    codigo = models.CharField(max_length=5, unique=True, editable=False)
    vendido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.gerar_codigo_unico()
        super().save(*args, **kwargs)

    def gerar_codigo_unico(self):
        codigo = str(random.randint(10000, 99999))
        while Produto.objects.filter(codigo=codigo).exists():
            codigo = str(random.randint(10000, 99999))
        return codigo

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

class PeriodoMeta(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='periodo_meta_empresa')
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=True, blank=True)
    valor_meta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_alcancado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fechado = models.BooleanField(default=False)
    foi_lucro = models.BooleanField(default=False)

    def __str__(self):
        return f"Meta {self.data_inicio.strftime('%B %Y')} - {self.empresa.nome}"

    def progresso(self):
        vendas_periodo = Venda.objects.filter(
            empresa=self.empresa,
            data_venda__gte=self.data_inicio,
            data_venda__lt=self.data_fim if self.data_fim else timezone.now()
        )

        total_vendas = 0
        for venda in vendas_periodo:
            itens_venda = ItemVenda.objects.filter(venda=venda)
            total_vendas += sum(item.quantidade * item.produto.preco for item in itens_venda)

        return total_vendas

    def falta_para_meta(self):
        return max(0, self.valor_meta - self.progresso())

    def lucro(self):
        return self.progresso()

FORMA_PAGAMENTO_CHOICES = [
    ('debito', 'Cartão de Débito'),
    ('credito', 'Cartão de Crédito'),
    ('pix', 'Pix'),
    ('credito_parcelado', 'Crédito Parcelado'),
    ('dinheiro', 'Dinheiro'),
    ('marcou', 'Marcou'),
]
class Venda(BaseModel):
    data_venda = models.DateTimeField(default=timezone.now)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor_vendas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='compras_clientes')
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    descricao = RichTextUploadingField("Descrição da venda:")
    periodometa = models.ForeignKey(PeriodoMeta, on_delete=models.CASCADE, related_name='periodo_meta_venda')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='venda_empresa', default=1)

    def __str__(self):
        return f"{self.vendedor} - {self.data_venda} unidades vendidas"

class ItemVenda(models.Model):
    venda = models.ForeignKey('Venda', on_delete=models.CASCADE, related_name='itens_venda')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='item_venda_produto')
    quantidade = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='venda_empresa_item', default=1)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"

STATUS_PEDIDO_CHOICES = [
    ('pendente', 'Pendente'),
    ('comprado', 'Comprado'),
    ('notificado', 'Notificado'),
]

class Pedido(BaseModel):
    cliente_nome = models.CharField(max_length=255)
    cliente_email = models.EmailField(blank=True, null=True)
    cliente_telefone = models.CharField(max_length=15, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='pedidos_clientes_produto', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos_clientes', blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor_pedidos')
    quantidade = models.PositiveIntegerField()
    data_pedido = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_PEDIDO_CHOICES, default='pendente')
    notificado = models.BooleanField(default=False)
    descricao = RichTextUploadingField("Descrição da venda:")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='pedido_empresa')

    def __str__(self):
        return f"Pedido de {self.cliente_nome} - {self.descricao}"

class ValePresente(BaseModel):
    STATUS_VALEPRESENTE_CHOICES = [
        ('pendente', 'Pendente'),
        ('comprado', 'Comprado'),
        ('notificado', 'Notificado'),
        ('expirado', 'Expirado'),
    ]
    # comprador
    cliente_nome = models.CharField(max_length=255)
    cliente_email = models.EmailField(blank=True, null=True)
    cliente_comprador = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='valepresente_cliente_comprador', blank=True, null=True)
    cliente_telefone = models.CharField(max_length=15, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='valepresente_cliente', blank=True, null=True)
    # ganhador
    cliente_ganhador_nome = models.CharField(max_length=255, blank=True, null=True)
    cliente_ganhador_telefone = models.CharField(max_length=15, blank=True, null=True)
    cliente_ganhador = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='valepresente_cliente_ganhador', blank=True, null=True)
    cliente_email_cliente_ganhador = models.EmailField(blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='valepresente_vendedor')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(default=timezone.now)
    data_periodo_final = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_VALEPRESENTE_CHOICES, default='pendente')
    descricao = RichTextUploadingField("Descrição da venda:")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='valepresente_empresa')

    def __str__(self):
        return f"Vale presente de {self.cliente_nome} - {self.descricao}"