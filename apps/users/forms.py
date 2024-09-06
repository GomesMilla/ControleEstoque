from django import forms
from .models import Empresa, User, Cliente

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'razao_social', 'email', 'descricao', 'logo', 'color', 'color_fonte', 'logo_navegador']
    
    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].label = "Descrição:"
        self.fields['descricao'].help_text = "Use esse campo para descrever maiores informações sobre sua empresa."
        self.fields['logo'].label = "Logo da barra de menu:"
        self.fields['logo'].help_text = "Logo da loja que estará presente na barra de menu."
        self.fields['color'].label = "Cor da barra de menu:"
        self.fields['color_fonte'].label = "Cor da letra da barra de menu:"
        self.fields['logo_navegador'].label = "Logo da aba do navegador."

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nome', 'cpf', 'email', 'imagemperfil', 'password', 'if_funcionario']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome Completo:"
        self.fields['cpf'].label = "CPF:"
        self.fields['cpf'].help_text = "O CPF será utilizado como forma de acesso ao sistema. Certifique-se de que não existe outro usuário com o mesmo CPF, pois ele é único para cada usuário."
        self.fields['email'].label = "E-mail:"
        self.fields['email'].help_text = "O E-mail será utilizado como forma de contato do sistema. Certifique-se de que não existe outro usuário com o mesmo e-mail, pois ele é único para cada usuário."
        self.fields['password'].label = "Senha:"
        self.fields['if_funcionario'].label = "Funcionário."
        self.fields['if_funcionario'].help_text = "Ao habilitar esta opção, fica explícito que o usuário é apenas funcionário. Caso contrário, ele será tratado como sócio e dono da empresa, podendo ver informações como metas e valores."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nome', 'cpf', 'email', 'imagemperfil', 'if_funcionario']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome Completo:"
        self.fields['cpf'].label = "CPF:"
        self.fields['cpf'].help_text = "O CPF será utilizado como forma de acesso ao sistema. Certifique-se de que não existe outro usuário com o mesmo CPF, pois ele é único para cada usuário."
        self.fields['email'].label = "E-mail:"
        self.fields['email'].help_text = "O E-mail será utilizado como forma de contato do sistema. Certifique-se de que não existe outro usuário com o mesmo e-mail, pois ele é único para cada usuário."
        self.fields['if_funcionario'].label = "Funcionário."
        self.fields['if_funcionario'].help_text = "Ao habilitar esta opção, fica explícito que o usuário é apenas funcionário. Caso contrário, ele será tratado como sócio e dono da empresa, podendo ver informações como metas e valores."

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class UserFormAdmin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nome', 'cpf', 'email', 'empresa','imagemperfil', 'password', 'if_funcionario']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'data_aniversario', 'telefone_celular', 'observacoes', 'cpf', 'genero']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome do Cliente(Obrigatório):"
        self.fields['data_aniversario'].label = "Data de Aniversário(Obrigatório):"
        self.fields['telefone_celular'].label = "Telefone celular(Obrigatório):"
        self.fields['observacoes'].label = "Observações:"
        self.fields['observacoes'].help_text = "DICA: Use esse campo para colocar maiores informações sobre o seu cliente."
        self.fields['cpf'].label = "CPF:"
        self.fields['genero'].label = "Gênero:"