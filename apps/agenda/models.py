from django.db import models
from users.models import Empresa, User
from ckeditor_uploader.fields import RichTextUploadingField

class Evento(models.Model):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    titulo = models.CharField(max_length=200)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='evento_empresa')

    def __str__(self):
        return self.titulo
