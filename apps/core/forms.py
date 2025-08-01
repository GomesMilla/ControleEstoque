from django import forms
from .models import Estoque, Produto

from django import forms
from .models import *
from users.models import Cliente
from django import forms
from .models import VendaFiado
from django_select2.forms import Select2Widget
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory, BaseInlineFormSet

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

class TamanhoForm(forms.ModelForm):
    class Meta:
        model = Tamanho
        fields = ['nome', 'descricao', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TamanhoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para detalhar o máximo possível de informações sobre o seu tamanho."
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False

class FornecedoresForm(forms.ModelForm):
    class Meta:
        model = Fornecedores
        fields = ['nome', 'razao_social', 'cnpj', 'endereco', 'cep', 'cidade', 'estado', 'inscricao_estadual', 'inscricao_municipal', 'telefone', 'email', 'site', 'localizacao', 'condicoes_pagamento', 'condicoes_entrega', 'historico_compras', 'avaliacao', 'descricao', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FornecedoresForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome(Obrigatório):"
        self.fields['razao_social'].label = "Razão Social:"
        self.fields['cnpj'].label = "CNPJ:"
        self.fields['endereco'].label = "Endereço:"
        self.fields['cep'].label = "CEP:"
        self.fields['cidade'].label = "Cidade:"
        self.fields['estado'].label = "Estado:"
        self.fields['localizacao'].label = "Localização:"
        self.fields['inscricao_estadual'].label = "Inscrição Estadual:"
        self.fields['inscricao_municipal'].label = "Inscrição Municipal:"
        self.fields['telefone'].label = "Telefone:"
        self.fields['email'].label = "E-mail:"
        self.fields['site'].label = "Site:"
        self.fields['site'].help_text = "DICA: Cole aqui a URL do site para que você possa ter essa informação cadastrada para possíveis pesquisas."        
        self.fields['condicoes_pagamento'].label = "Condições de Pagamento:"
        self.fields['condicoes_pagamento'].help_text = "DICA: Use esse campo para descrever as formas de pagamentos que ele aceita."
        self.fields['condicoes_entrega'].label = "Condições de Entrega:"
        self.fields['condicoes_entrega'].help_text = "DICA: Use esse campo para descrever as formas de entrega que ele aceita."
        self.fields['historico_compras'].label = "Histórico de Compras:"
        self.fields['historico_compras'].help_text = "DICA: Use esse campo para descrever as formas descrever um breve resumo sobre o histórico de compras se foi válido ou não."
        self.fields['avaliacao'].label = "Avaliação:"
        self.fields['avaliacao'].help_text = "DICA: Use esse campo para avaliar a satisfação com o fornecedor."
        self.fields['descricao'].label = "Descrição(Obrigatório):"
        self.fields['descricao'].help_text = "DICA: Use esse campo para detalhar o máximo possível de informações sobre o seu fornecedor."
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False

class TipoProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = ['nome', 'descricao', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TipoProdutoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para detalhar o máximo possível de informações sobre o seu tipo de produto."
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome', 'descricao', 'logo', 'site', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MarcaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome da marca:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['logo'].label = "Logo da marca:"
        self.fields['site'].label = "URL da marca:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para detalhar o máximo possível de informações sobre a marca."
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome','cor','tamanho','marca','tipo_produto','fornecedor','descricao', 'preco','preco_custo','quantidade', 'imagemperfil', 'estoque', 'empresa', 'is_promocao' ]
        widgets = {
            'fornecedor': Select2Widget(attrs={'data-minimum-input-length': 1}),
            'tamanho': Select2Widget(attrs={'data-minimum-input-length': 1}),
            'tipo_produto': Select2Widget(attrs={'data-minimum-input-length': 1}),
            'marca': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para descrever maiores informações sobre o(s) produto(s) e também sua localização."
        self.fields['preco'].label = "Preço de Venda:"
        self.fields['quantidade'].label = "Quantidade:"
        self.fields['imagemperfil'].label = "Foto do Produto:"
        self.fields['estoque'].label = "Estoque:"
        self.fields['preco_custo'].label = "Preço de Custo:"

        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['estoque'].queryset = Estoque.objects.filter(empresa=user.empresa)
            self.fields['fornecedor'].queryset = Fornecedores.objects.filter(empresa=user.empresa)
            self.fields['tamanho'].queryset = Tamanho.objects.filter(empresa=user.empresa)
            self.fields['marca'].queryset = Marca.objects.filter(empresa=user.empresa)
            self.fields['tipo_produto'].queryset = TipoProduto.objects.filter(empresa=user.empresa)
            self.fields['empresa'].required = False
        else:
            self.fields['estoque'].queryset = Estoque.objects.none()
            self.fields['fornecedor'].queryset = Fornecedores.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        if empresa:
            self.fields['estoque'].queryset = Estoque.objects.filter(empresa=empresa)
        return cleaned_data

class PeriodoMetaForm(forms.ModelForm):
    class Meta:
        model = PeriodoMeta
        fields = ['nome', 'data_inicio', 'valor_meta', 'descricao']

    def __init__(self, *args, **kwargs):
        super(PeriodoMetaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].required = True
        self.fields['data_inicio'].label = "Data de Início da meta:"
        self.fields['data_inicio'].help_text = "A meta será uma forma de organizar a gestão das suas vendas."
        self.fields['valor_meta'].label = "Valor da Meta:"
        self.fields['valor_meta'].help_text = "Valor de vendas planejado para a meta."
        self.fields['descricao'].label = "Observação:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para descrever sobre seu planejamento para essa meta."

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nome', 'cliente_email', 'cliente_telefone', 'produto', 'cliente', 'quantidade', 'descricao', 'status']
        widgets = {
            'cliente': Select2Widget(attrs={'data-minimum-input-length': 1}),
            'produto': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }

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
        widgets = {
            'cliente': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }
    
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
        widgets = {
            'produto': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }

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
        widgets = {
            'cliente': Select2Widget(attrs={'data-minimum-input-length': 1}),
            'cliente_ganhador': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }

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

class ContaCorrenteForm(forms.ModelForm):
    class Meta:
        model = ContaCorrente
        fields = ['cliente', 'descricao', 'limite_credito']
        widgets = {
            'cliente': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['descricao'].label = "Descrição da Conta:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para melhor descrever as informações sobre o seu cliente e sobre a conta dele. Para ajuda-lá na hora de gerenciar."

    def save(self, commit=True):
        conta_corrente = super().save(commit=False)
        conta_corrente.empresa = self.user.empresa
        if commit:
            conta_corrente.save()
        return conta_corrente

class VendaFiadoForm(forms.ModelForm):
    class Meta:
        model = VendaFiado
        fields = ['cliente', 'conta_corrente', 'num_parcelas', 'dia_vencimento', 'descricao']
        widgets = {
            'cliente': Select2Widget(attrs={'data-minimum-input-length': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['cliente'].label = "Cliente:"
        self.fields['conta_corrente'].label = "Conta:"
        self.fields['num_parcelas'].label = "Número de parcelas:"
        self.fields['descricao'].help_text = "Use esse campo para maiores informações sobre a venda."

        if self.user and hasattr(self.user, 'empresa') and self.user.empresa:
            self.fields['conta_corrente'].queryset = ContaCorrente.objects.filter(empresa=self.user.empresa)
        else:
            self.fields['conta_corrente'].queryset = ContaCorrente.objects.none()

class ItemVendaFiadoForm(forms.ModelForm):
    class Meta:
        model = ItemVendaFiado
        fields = ['produto', 'quantidade']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


# Formset para gerenciar múltiplos itens de venda
class BaseItemVendaFiadoFormset(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        """Passa o user para cada formulário individual no formset."""
        kwargs['user'] = self.user
        return super()._construct_form(i, **kwargs)

ItemVendaFiadoFormset = modelformset_factory(
    ItemVendaFiado,
    form=ItemVendaFiadoForm,
    extra=1,
    formset=BaseItemVendaFiadoFormset
)

class BaseItemVendaInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super()._construct_form(i, **kwargs)

ItemVendaFormset = inlineformset_factory(
    Venda,
    ItemVenda,
    form=ItemVendaForm,
    extra=1,
    can_delete=True,
    formset=BaseItemVendaInlineFormset
)

def form_valid(self, form):
    form.instance.vendedor = self.request.user
    form.instance.empresa = self.request.user.empresa
    form.instance.periodometa = get_object_or_404(PeriodoMeta, fechado=False, empresa=self.request.user.empresa)
    from django.db import transaction
    with transaction.atomic():
        # 1. Salva a venda primeiro
        self.object = form.save(commit=False)
        # 2. Cria o formset já vinculado à venda criada
        item_formset = ItemVendaFormset(self.request.POST, instance=self.object, user=self.request.user)
        # 3. Valida o formset
        if item_formset.is_valid():
            itens = item_formset.save(commit=False)
            for item in itens:
                produto = item.produto
                quantidade = item.quantidade
                if produto.quantidade < quantidade:
                    item_formset.add_error(None, f'Quantidade insuficiente no estoque para {produto.nome}.')
                    transaction.set_rollback(True)
                    return self.form_invalid(form)
                produto.quantidade -= quantidade
                if produto.quantidade <= 0:
                    produto.quantidade = 0
                    produto.vendido = True
                produto.save()
                item.empresa = self.request.user.empresa
                item.save()
            item_formset.save_m2m()
            return super().form_valid(form)
        else:
            self.object.delete()
            return self.form_invalid(form)




