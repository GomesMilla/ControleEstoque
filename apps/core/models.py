from django.db import models
from users.models import User, Empresa, BaseModel, Cliente
import random
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F
class Estoque(BaseModel):
    nome = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='estoques')
    localizacao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Fornecedores(BaseModel):
    nome = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    inscricao_estadual = models.CharField(max_length=50, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=50, blank=True, null=True)

    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    site = models.URLField(max_length=255, blank=True, null=True)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    condicoes_pagamento = models.TextField(blank=True, null=True)
    condicoes_entrega = models.TextField(blank=True, null=True)
    historico_compras = models.TextField(blank=True, null=True)

    avaliacao = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    descricao = RichTextUploadingField("Descrição do produto:")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fornecedores_empresa')

    def __str__(self):
        return self.nome

class Tamanho(BaseModel):
    nome = models.CharField(max_length=255)
    descricao = RichTextUploadingField("Descrição do tamanho:", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tamanho_empresa')

    def __str__(self):
        return self.nome

class TipoProduto(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = RichTextUploadingField("Descrição do tipo de produto:", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tipoproduto_empresa', null=True, blank=True)

    def __str__(self):
        return self.nome

class Marca(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = RichTextUploadingField("Descrição do produto:", null=True, blank=True)
    logo = models.ImageField(upload_to='logos_marcas/', null=True, blank=True)
    site = models.URLField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='marcar_empresa', null=True, blank=True)

    def __str__(self):
        return self.nome

class Produto(BaseModel):
    nome = models.CharField(max_length=255)
    cor = models.CharField(max_length=50, null=True, blank=True)
    descricao = RichTextUploadingField("Descrição do produto:")
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantidade = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produtos')
    imagemperfil = models.ImageField("Foto de Produto", upload_to="fotoproduto/", null=True, blank=True)
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='produto_estoque')
    codigo = models.CharField(max_length=5, unique=True, editable=False)
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.SET_NULL, null=True, blank=True, related_name='produtos_fornecedor')
    vendido = models.BooleanField(default=False)
    is_promocao = models.BooleanField("Produto em promoção",default=False)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.SET_NULL, related_name='tipo_produto', null=True, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL,related_name='marca_produto', null=True, blank=True)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.SET_NULL, related_name='tamanho_produto', null=True, blank=True)

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

    @property
    def lucro(self):
        lucro_unitario = self.preco - self.preco_custo
        return lucro_unitario * self.quantidade 

class PeriodoMeta(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='periodo_meta_empresa')
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=True, blank=True)
    valor_meta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_alcancado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fechado = models.BooleanField(default=False)
    foi_lucro = models.BooleanField(default=False)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)

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
    
    def recebimentos_parcelas(self):
        parcelas_pagas = Parcela.objects.filter(
            venda__empresa=self.empresa,
            data_atualizacao__gte=self.data_inicio,
            data_atualizacao__lt=self.data_fim if self.data_fim else timezone.now(),
            pendente=False  # Apenas parcelas pagas
        )

        total_recebido_parcelas = parcelas_pagas.aggregate(total=Sum('valor'))['total'] or 0
        return total_recebido_parcelas
    
    def relatorio_meta(self):
        vendas_lucro = self.lucro()
        parcelas_lucro = self.recebimentos_parcelas()

        return {
            'lucro_vendas': vendas_lucro,
            'lucro_parcelas': parcelas_lucro,
            'lucro_total': vendas_lucro + parcelas_lucro,
            'numero_vendas': self.numero_vendas(),
            'numero_parcelas_pagas': self.numero_parcelas_pagas(),
            'porcentagem_alcancada': self.porcentagem_alcancada(),
            'falta_para_meta': self.falta_para_meta(),
        }
    
    def numero_vendas(self):
        return Venda.objects.filter(
            empresa=self.empresa,
            data_venda__gte=self.data_inicio,
            data_venda__lt=self.data_fim if self.data_fim else timezone.now()
        ).count()

    def numero_parcelas_pagas(self):
        return Parcela.objects.filter(
            venda__empresa=self.empresa,
            data_atualizacao__gte=self.data_inicio,
            data_atualizacao__lt=self.data_fim if self.data_fim else timezone.now(),
            pendente=False
        ).count()

    def porcentagem_alcancada(self):
        if self.valor_meta > 0:
            return (self.progresso() / self.valor_meta) * 100
        return 0



FORMA_PAGAMENTO_CHOICES = [
    ('debito', 'Cartão de Débito'),
    ('pix', 'Pix'),
    ('dinheiro', 'Dinheiro'),
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
        ('cancelado', 'Cancelado'),
    ]
    # comprador
    cliente_nome = models.CharField(max_length=255)
    cliente_email = models.EmailField(blank=True, null=True)
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
class ContaCorrente(BaseModel):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='conta_corrente')
    descricao = RichTextUploadingField("Descrição da venda:")
    saldo_devedor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='conta_corrente_empresa')

    def atualizar_saldo(self, valor):
        """Atualiza o saldo devedor com a nova compra fiada."""
        self.saldo_devedor += valor
        self.save()

    def reduzir_saldo(self, valor):
        """Reduz o saldo devedor ao registrar o pagamento de uma parcela."""
        self.saldo_devedor -= valor
        self.save()

    def __str__(self):
        return f"Conta de {self.cliente.nome}"

class VendaFiado(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    conta_corrente = models.ForeignKey(ContaCorrente, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    num_parcelas = models.PositiveIntegerField()
    dia_vencimento = models.PositiveIntegerField()
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor_venda_fiado')
    descricao = RichTextUploadingField("Descrição da venda:")
    periodometa = models.ForeignKey(PeriodoMeta, on_delete=models.CASCADE, related_name='periodo_meta_venda_fiado')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='venda_fiado_empresa', default=1)
    
    def __str__(self):
        return f"Venda fiado de {self.cliente.nome} - {self.data_venda}"

    def gerar_parcelas(self):
        """Gera as parcelas da venda fiado."""
        valor_parcela = round(self.total / self.num_parcelas, 2)
        for i in range(self.num_parcelas):
            vencimento = self.data_venda + relativedelta(months=i, day=self.dia_vencimento)
            Parcela.objects.create(
                venda=self,
                valor=valor_parcela,
                data_vencimento=vencimento,
                pendente=True,
                empresa=self.empresa  # Vinculando à empresa
            )
class Parcela(BaseModel):
    venda = models.ForeignKey(VendaFiado, on_delete=models.CASCADE, related_name='parcelas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pendente = models.BooleanField(max_length=20, default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='parcela_fiado_empresa', default=1)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor_venda_recebeu_valor', null=True, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return f"Parcela de {self.valor} com vencimento em {self.data_vencimento}"

class ItemVendaFiado(models.Model):
    venda = models.ForeignKey(VendaFiado, on_delete=models.CASCADE, related_name='itens_venda')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='venda_afido_empresa_item', default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
