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

