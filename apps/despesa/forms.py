from django import forms
from .models import TipoDespesa, Despesa

class TipodeDespesaForm(forms.ModelForm):
    class Meta:
        model = TipoDespesa
        fields = ['nome', 'empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TipodeDespesaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome do Tipo de Despesa:"
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['titulo', 'descricao', 'valor', 'data', 'tipo', 'eh_extra','despesa_paga','empresa']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DespesaForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].label = "Título:"
        self.fields['data'].label = "Data de Pagamento:"
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()
            self.fields['empresa'].required = False
            self.fields['tipo'].queryset = TipoDespesa.objects.filter(empresa=user.empresa)