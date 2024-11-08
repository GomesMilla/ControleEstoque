from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.db import IntegrityError
from colorfield.fields import ColorField
from django.core.validators import RegexValidator
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
class UserManager(BaseUserManager):
    def get_or_create(self, defaults=None, **kwargs):
        try:
            user = self.get(**kwargs)
            if user.excluido or not user.is_active:
                user.excluido = False
                user.is_active = True
                user.save()
            return user, False
        except self.model.DoesNotExist:
            return self._create_user(**kwargs, defaults=defaults), True

    def _create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("Usuário deve ter um CPF válido")

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(cpf, email, password, **extra_fields)

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(cpf, email, password, **extra_fields)

    def get_queryset(self):
        return super(UserManager, self).get_queryset().exclude(is_active=False).exclude(excluido=True)

    def todos_usuarios(self):
        return super(UserManager, self).get_queryset()

class BaseModel(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    data_desativacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Empresa(BaseModel):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField('CNPJ',max_length=18, blank=True, null=True)
    razao_social = models.CharField('Razão Social', max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name="Endereço de E-mail", max_length=255, unique=True, null=True, blank=True)
    descricao = RichTextUploadingField("Observação:", blank=True, null=True)
    logo = models.ImageField("Logo", upload_to="logo/")  
    color = ColorField(format="hexa")
    color_fonte = ColorField(format="hexa", blank=True, null=True)
    logo_navegador = models.ImageField("Logo", upload_to="logonavegador/", blank=True, null=True)
    agenda = models.BooleanField("Liberar funcionalidade de agenda", default=False)
    lista_produto = models.BooleanField("Liberar funcionalidade de lista de produto", default=False)
    telefonedecontato = models.CharField('Número de telefone', max_length=18, blank=True, null=True)
    resumo_loja = models.TextField('Resumo', blank=True, null=True) 

    def __str__(self):
        return self.nome

    def __str__(self):
        return self.nome


THEME_CHOICES = [
    ("dark", "Dark"),
    ("light", "Light"),
    ("auto", "Auto"),
]
class User(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField('CPF', max_length=18, unique=True)
    email = models.EmailField(verbose_name="Endereço de E-mail", max_length=255, unique=True, null=True, blank=True)
    telefone_celular = models.CharField(max_length=15, null=True, blank=True)
    descricao = RichTextUploadingField("Observações:", null=True, blank=True)
    imagemperfil = models.ImageField("Foto de Perfil", upload_to="ImagemPerfil/")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')    
    theme = models.CharField(max_length=5, default="dark", choices=THEME_CHOICES)
    if_funcionario = models.BooleanField(default=True) #define se é socio ou apenas funcionário.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    excluido = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_desativacao = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.pk:
            usuarios_qs = User.objects.todos_usuarios().filter(Q(excluido=True) | Q(is_active=False), cpf=self.cpf)
            if usuarios_qs.exists():
                usuario_existente = usuarios_qs.first()
                usuario_existente.is_active = True
                usuario_existente.excluido = False
                usuario_existente.save()
                return usuario_existente
        return super().save(*args, **kwargs)

    def get_short_name(self):
        return self.cpf


class ProfileManager(BaseUserManager):
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().exclude(user__is_active=False).exclude(user__excluido=True)

    def todos_usuarios(self):
        return super(ProfileManager, self).get_queryset()

    def usuarios_inativos(self):
        return super(ProfileManager, self).get_queryset().filter(user__is_active=False)

    def usuarios_ativos(self):
        return super(ProfileManager, self).get_queryset().filter(user__is_active=True)


class Cliente(BaseModel):
    nome = models.CharField(max_length=255)
    data_aniversario = models.DateField()
    telefone_celular = models.CharField(max_length=15)
    observacoes = RichTextUploadingField("Observação:", blank=True, null=True)
    cpf = models.CharField('CPF', max_length=18, blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='clientes_empresa')

    def __str__(self):
        return self.nome
