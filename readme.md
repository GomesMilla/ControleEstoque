<h1 align="center">Controle de Estoque</h1>
<p>Sistema completo de controle de estoque para lojas, oferecendo uma solução eficiente para gestão de produtos, vendas, clientes e mais.</p>
<h4 align="center"> 
	🚧  Status 🚀 Desenvolvendo o código  🚧
</h4>

<!-- <h1 align="center">
  <img alt="Imagem de inicio" title="#ControleDeEstoque" src="staticFile/imagens/Apresentação.png" />
</h1> -->
<p text-align="justify">Este repositório tem foco, na criação de uma aplicação de Controle de Estoque de um estabelecimento, interligado a um banco de dados provido pelo próprio Framework Django facilitando dessa forma a manipulação de seus dados.</p>
<p text-align="justify">Este projeto faz parte do meu portfólio pessoal, então, ficarei feliz caso você forneça algum feedback, código, estrutura, funcionalidade ou qualquer melhoria que você possa relatar para melhora-lo.Você pode usar este projeto como quiser, seja para estudar, fazer melhorias, você quem manda!.</p>

<blockquote>
Este é um projeto totalmente grátis!
</blockquote>

### 🏁 Funcionalidades Principais

- [x] Gestão de Produtos: Cadastro, atualização e exclusão de produtos com controle detalhado de informações como categorias, tamanhos e preços.
- [x] Controle de Estoque: Monitora entradas e saídas de estoque, garantindo que a quantidade disponível de cada produto esteja sempre atualizada.
- [x] Gestão de Vendas: Facilita o processo de venda, integrando controle de estoque com registro de pedidos e emissão de relatórios de vendas.
- [x] Gestão de Clientes: Cadastro e acompanhamento de clientes, permitindo a visualização de históricos de compra e informações relevantes.
- [x] Controle de Despesas: Registra e acompanha despesas da loja, oferecendo uma visão financeira clara.
- [x] Gestão de Pedidos: Organiza e gerencia pedidos realizados, com controle de status e alertas para acompanhamento.
- [x] Agendas: Gerencia compromissos e eventos da loja, como recebimento de mercadorias ou reuniões.
- [x] Relatórios Personalizados: Gera relatórios completos de vendas, produtos e movimentações de estoque, oferecendo insights para otimizar a operação.


### 🏁 Features

- [x] Cadastro de Usuário
- [x] Cadastro de Produto
- [x] Cadastro de Empresa
- [x] Cadastro de Vendedor
- [x] Listagem de Produtos
- [x] Listagem de Empresa
- [x] Listagem de Gerentes
- [ ] Deletar Produto
- [X] Desativar Empresa
- [ ] Deletar Vendedor
- [x] Login
- [x] Reset de senha
- [ ] PDF com as informações das movimentações do mês
- [ ] Acessando Informações Filtradas



### 🛠 Tecnologias
<p>As seguintes ferramentas foram usadas na construção do projeto:</p>

- [Django](https://www.djangoproject.com/start/)
- [Bootstrap](https://getbootstrap.com/)


### ⚠️ Warning
<p>Esse código é uma refatoração do meu antigo projeto que esta disponivel aqui no meu GitHub. Ele possui mais funcionalidades e identação de código</p>

- [Controle-de-estoque](https://github.com/GomesMilla/Controle-de-estoque)

<h1>Rodando o projeto</h1>
<h4>Clonando o projeto</h4>
<p>Dentro da pasta onde o projeto ficará armazenado, abra o terminal.</p>

<h5>Clonando via HTTPS:</h5>


```
git init
https://github.com/GomesMilla/ControleDeEstoque.git
cd ControleDeEstoque

```
<blockquote>
  Contribuição: Pull requests são bem-vindos! Para mudanças maiores, por favor abra uma issue antes para discutir o que você gostaria de alterar.
</blockquote>



<h4>Linux</h4>
<blockquote>
  Observação: Foi utilizado a distro Linux Mint(versão 20.1), caso ocorra algum problema na instalação, pesquise por conta própria a resolução do mesmo!
</blockquote>
<h4>Linux</h4>

``` 
sudo apt-get install python3-venv
```

<h4>Preparando o Projeto</h4>

```
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations Usuarios
python manage.py makemigrations Estoque
python manage.py makemigrations Transacao
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```

### Autor
---


 <img style="border-radius: 50%;" src="static/imagens/download.png" width="100px;" alt=""/>
 <sub><b>Camila Adriana</b></sub></a> <a href="www.linkedin.com/in/camila-adriana-gomes-de-jesus-04767b1ba" title="Foto de perfil"></a><br>
Feito com ❤️ por Camila Adriana 👋🏽 Entre em contato!

[![Twitter Badge](https://img.shields.io/badge/-@camilaA58109563-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=twitter&logoColor=white&link=https://twitter.com/Camila)](https://twitter.com/CamilaA58109563?s=09) [![Linkedin Badge](https://img.shields.io/badge/-Camila-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/Camila/)](https://www.linkedin.com/in/camila-adriana-gomes-de-jesus-04767b1ba/) 
