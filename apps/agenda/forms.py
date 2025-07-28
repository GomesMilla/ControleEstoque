from django import forms

from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'resumo', 'tipo', 'prioridade', 'recorrencia', 'data_fim_recorrencia' , 'descricao','data_inicio', 'data_fim', 'empresa']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].label = "Título do Evento:"
        self.fields['resumo'].label = "Resumo:"
        self.fields['tipo'].help_text = "Defina o tipo do evento para melhorar sua exibição e facilitar a organização."
        self.fields['prioridade'].help_text = "Defina a prioridade do evento para destacar sua importância na agenda."
        self.fields['recorrencia'].help_text = "Selecione a frequência com que o evento se repete, se aplicável."
        self.fields['recorrencia'].label = "Recorrência"
        self.fields['data_fim_recorrencia'].label = "Data Fim da Recorrência"
        self.fields['data_fim_recorrencia'].help_text = "Informe até quando o evento deve se repetir automaticamente."
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "DICA: Use esse campo para descrever maiores informações sobre o seu evento."
        self.fields['data_inicio'].label = "Data Ínicio:"
        self.fields['data_fim'].label = "Data Fim:"
        
        if not user.is_superuser:
            self.fields['empresa'].widget = forms.HiddenInput()