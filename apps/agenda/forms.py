from django import forms

from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'resumo', 'descricao','data_inicio', 'data_fim', 'empresa']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].label = "Título do evento:"
        self.fields['resumo'].label = "Resumo:"
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para descrever maiores informações sobre o seu evento."
        self.fields['data_inicio'].label = "Data Ínicio:"
        self.fields['data_fim'].label = "Data Fim:"
        
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()