from django import forms
from .models import Estoque, Produto

from django import forms
from .models import Estoque, Empresa, PeriodoMeta, Pedido, Venda, ItemVenda, ValePresente
from users.models import Cliente

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['nome', 'localizacao', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EstoqueForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome do Estoque:"
        self.fields['localizacao'].label = "Localização:"
        self.fields['localizacao'].help_text = "Localização do Estoque."
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'imagemperfil', 'estoque', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para descrever maiores informações sobre o(s) produto(s) e também sua localização."
        self.fields['preco'].label = "Preço:"
        self.fields['quantidade'].label = "Quantidade:"
        self.fields['imagemperfil'].label = "Foto do Produto:"
        self.fields['estoque'].label = "Estoque:"

        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['estoque'].queryset = Estoque.objects.filter(empresa=user.empresa)
            self.fields['empresa'].required = False
        else:
            self.fields['estoque'].queryset = Estoque.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        if empresa:
            self.fields['estoque'].queryset = Estoque.objects.filter(empresa=empresa)
        return cleaned_data

class PeriodoMetaForm(forms.ModelForm):
    class Meta:
        model = PeriodoMeta
        fields = ['nome', 'data_inicio', 'valor_meta']

    def __init__(self, *args, **kwargs):
        super(PeriodoMetaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].required = True
        self.fields['data_inicio'].label = "Data de Início da meta:"
        self.fields['data_inicio'].help_text = "A meta será uma forma de organizar a gestão das suas vendas."
        self.fields['valor_meta'].label = "Valor da Meta:"
        self.fields['valor_meta'].help_text = "Valor de vendas planejado para a meta."

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nome', 'cliente_email', 'cliente_telefone', 'produto', 'cliente', 'quantidade', 'descricao', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields['cliente_nome'].label = "Nome do Cliente (Obrigatório):"
        self.fields['cliente_email'].label = "E-mail do Cliente:"
        self.fields['cliente_telefone'].label = "Telefone do Cliente:"
        self.fields['produto'].label = "Produto:"
        self.fields['produto'].help_text = "DICA: Use esse campo quando for pedido um produto no qual já tenha ou teve em seu estoque."
        self.fields['cliente'].label = "Cliente:"
        self.fields['quantidade'].label = "Quantidade:"
        self.fields['descricao'].label = "Descrição do pedido e seu produto:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para melhor descrever as informações sobre o seu produto. Para ajuda-lá na hora de verificar com o fornecedor."
        self.fields['status'].label = "Status do Pedido:"
        if user and not user.is_superuser:
            # Filtra os produtos para exibir apenas aqueles pertencentes à empresa do usuário logado
            self.fields['produto'].queryset = Produto.objects.filter(empresa=user.empresa)

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'forma_pagamento', 'descricao']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VendaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].label = "Cliente:"
        self.fields['forma_pagamento'].label = "Forma de Pagamento:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para descrever maiores informações sobre a venda para melhor controle e gestão."
        if user and user.empresa:
            # Filtra os produtos para exibir apenas aqueles pertencentes à empresa do usuário logado
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=user.empresa)

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ItemVendaForm, self).__init__(*args, **kwargs)
        self.fields['produto'].label = "Produto:"
        self.fields['quantidade'].label = "Quantidade:"
        self.fields['quantidade'].help_text = "AVISO: Cuidado para que a quantidade de produto da venda, não seja superior a quantidade cadastrada no estoque."
        if user and user.empresa:
            self.fields['produto'].queryset = Produto.objects.filter(empresa=user.empresa, vendido=False)

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser um valor positivo.")
        return quantidade


class ValePresenteForm(forms.ModelForm):
    # Form para a criação do Vale Presente
    class Meta:
        model = ValePresente
        fields = ['cliente_nome', 'cliente' ,'cliente_email', 'cliente_telefone', 'cliente_ganhador_nome', 'cliente_ganhador', 'cliente_ganhador_telefone','cliente_email_cliente_ganhador' ,'cliente_ganhador', 'preco', 'descricao', 'data_periodo_final']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ValePresenteForm, self).__init__(*args, **kwargs)
        self.fields['cliente_nome'].label = "Nome do Cliente Comprador (Obrigatório):"
        self.fields['cliente_email'].label = "E-mail do Cliente Comprador:"
        self.fields['cliente_telefone'].label = "Telefone do Cliente Comprador:"
        self.fields['cliente'].label = "Cliente Comprador:"
        self.fields['cliente_ganhador'].label = "Cliente Ganhador (Obrigatório):"
        self.fields['cliente_ganhador_nome'].label = "Nome do Cliente Ganhador (Obrigatório):"
        self.fields['cliente_email_cliente_ganhador'].label = "E-mail do Cliente Ganhador:"
        self.fields['cliente_ganhador_telefone'].label = "Telefone do Cliente Ganhador:"
        self.fields['cliente_ganhador'].label = "Cliente Ganhador:"
        self.fields['preco'].label = "Preço:"
        self.fields['descricao'].label = "Descrição do pedido e seu produto:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para melhor descrever as informações sobre o seu vale. Para ajuda-lá na hora de gerenciar."

class ValePresenteUpdateForm(forms.ModelForm):
    # Form para a criação do Vale Presente
    class Meta:
        model = ValePresente
        fields = ['cliente_nome', 'cliente' ,'cliente_email', 'cliente_telefone', 'cliente_ganhador_nome' , 'cliente_ganhador', 'cliente_ganhador_telefone','cliente_email_cliente_ganhador' ,'cliente_ganhador', 'preco', 'descricao', 'data_periodo_final', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ValePresenteUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cliente_nome'].label = "Nome do Cliente Comprador: (Obrigatório)"
        self.fields['cliente_email'].label = "E-mail do Cliente Comprador:"
        self.fields['cliente_telefone'].label = "Telefone do Cliente Comprador: (Obrigatório)"
        self.fields['cliente'].label = "Cliente Comprador:"
        self.fields['cliente_ganhador_nome'].label = "Nome do Cliente Ganhador: (Obrigatório)"
        self.fields['cliente_email_cliente_ganhador'].label = "E-mail do Cliente Ganhador:"
        self.fields['cliente_ganhador_telefone'].label = "Telefone do Cliente Ganhador:"
        self.fields['cliente_ganhador'].label = "Cliente Ganhador:"
        self.fields['preco'].label = "Preço:"
        self.fields['descricao'].label = "Descrição do pedido e seu produto:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para melhor descrever as informações sobre o seu vale. Para ajuda-lá na hora de gerenciar."