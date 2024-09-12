from django.db import models
from users.models import Empresa, User, BaseModel
from ckeditor_uploader.fields import RichTextUploadingField

class Evento(BaseModel):
    """ Event model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    titulo = models.CharField(max_length=200)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)
    resumo = models.TextField(null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
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



