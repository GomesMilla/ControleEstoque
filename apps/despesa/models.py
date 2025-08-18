from django.db import models
from users.models import Empresa, User, BaseModel
from ckeditor_uploader.fields import RichTextUploadingField

class TipoDespesa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tipo_despesa_empresa', null=True, blank=True)

    def __str__(self):
        return self.nome

class Despesa(BaseModel):
    titulo = models.CharField("Descrição", max_length=250)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    data = models.DateField("Data")
    tipo = models.ForeignKey(TipoDespesa, on_delete=models.CASCADE, verbose_name="Tipo de Despesa")
    eh_extra = models.BooleanField("É despesa extra?", default=False)
    despesa_paga = models.BooleanField("Despesa Paga", default=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='despesa_empresa', null=True, blank=True)

    def __str__(self):
        return f"{self.descricao} - R${self.valor}"

