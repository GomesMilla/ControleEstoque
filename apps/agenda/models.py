from django.db import models
from users.models import Empresa, User, BaseModel
from ckeditor_uploader.fields import RichTextUploadingField

TIPO_EVENTO_CHOICES = [
    ('conta_pagar', 'Conta a Pagar'),
    ('conta_receber', 'Conta a Receber'),
    ('pagamento_funcionario', 'Pagamento de Funcionários'),
    ('imposto', 'Impostos e Tributos'),
    ('reembolso', 'Reembolso'),
    ('brinde', 'Envio de Brinde'),
    ('promocao', 'Ação Promocional'),
    ('contato_cliente', 'Contato com Cliente'),
    ('renovacao_contrato', 'Renovação de Contrato'),
    ('proposta', 'Proposta Comercial'),
    ('entrega', 'Entrega Agendada'),
    ('reuniao', 'Reunião Interna'),
    ('visita_tecnica', 'Visita Técnica'),
    ('treinamento', 'Treinamento / Capacitação'),
    ('manutencao', 'Manutenção'),
    ('aniversario_cliente', 'Aniversário de Cliente'),
    ('aniversario_funcionario', 'Aniversário de Funcionário'),
    ('feriado', 'Feriado'),
    ('data_comemorativa', 'Data Comemorativa'),
    ('outros', 'Outros'),
]

PRIORIDADE_CHOICES = [
    ('baixa', 'Baixa'),
    ('media', 'Média'),
    ('alta', 'Alta'),
    ('urgente', 'Urgente'),
]

RECORRENCIA_CHOICES = [
    ('semanal', 'Semanalmente'),
    ('quinzenal', 'Quinzenalmente'),
    ('mensal', 'Mensalmente'),
    ('anual', 'Anualmente'),
]


class Evento(BaseModel):
    """ Event model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    titulo = models.CharField(max_length=200)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)
    resumo = models.TextField(null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.CharField(max_length=30, choices=TIPO_EVENTO_CHOICES, default='outros')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='baixa')
    recorrencia = models.CharField(max_length=15, choices=RECORRENCIA_CHOICES, blank=True, null=True, default=None, help_text="Repetição automática do evento (opcional)")
    data_fim_recorrencia = models.DateField(blank=True, null=True, help_text="Data final para repetir o evento (opcional)")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='evento_empresa', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Alerta(BaseModel):
    """ Alerta model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerta")
    titulo = models.CharField(max_length=200)
    resumo = models.TextField("Resumo",null=True, blank=True)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_alerta', null=True, blank=True)

    def __str__(self):
        return self.titulo



