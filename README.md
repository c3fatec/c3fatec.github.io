

<div align="center">
    
![banner](https://i.ibb.co/QDpNydM/APRESENTA-O-C3-1-SPRINT-Capa-para-Facebook.jpg)


</div>
<br id="topo">
<p align="center">
    <a href="#sobre">Sobre</a>  |  
    <a href="#backlogs">Product Backlog</a>  |  
    <a href="#sprints">Sprints</a>  |  
    <a href="#tecnologias">Tecnologias</a>  |  
    <a href="#equipe">Equipe</a> |
    <a href="#instruções">Instruções</a>
</p>

## :bookmark_tabs: Sobre 
Esse repositório contém o primeiro projeto API dos estudantes do primeiro semestre 2022/2 de DSM da Fatec de São José dos Campos. O projeto propõe a criação de uma aplicação que simule um banco digital, com funcionalidades para criação e manutenção de uma conta de usuário, gerenciamento interno e display responsivo para web.

----------
## :date: Sprints

| Sprint | Data Final | Status | 
|:--:|:----------:|:----------------|:----------------------------------:|
| 01 | 18/09/2022 | ✔️ Concluída    | 
| 02 | 19/10/2022 | ✔️ Concluída    | 
| 03 | 06/11/2022 |   | 
| 04 | 27/11/2022 |   | 


----------

## :open_file_folder:Product Backlog
<h4>1º Sprint -  <a href="https://i.ibb.co/TgW062T/pb1.png">Clique aqui</a>

<h4>2º Sprint</h4>    
<img src="https://i.ibb.co/M6n9cFr/Product-Backlog.jpg" alt="Product-Backlog" border="0">

----------
## :computer:Tecnologias Utilizadas

<img src="https://i.ibb.co/pfvD7fv/Tecnologiasc3.jpg" alt="Tecnologiasc3" border="0">


## :busts_in_silhouette:Equipe 

|    Função     |                  Nome                 |                       
| :-----------: | :------------------------------------ | 
| Product Owner | Daniel Machado dos Santos             |           
| Scrum Master  | Gabriel Oliveira Santos               |  
|   Dev Team    | Ivan Suiyma                           | 
|   Dev Team    | Jackles Kerley                        |   
|   Dev Team    | Claudinei Paulista                    |                     
----------
## :gear:Instruções 

 **Instalando o projeto**

Para rodar o projeto em sua máquina, inicie um ambiente virtual:
```
pip install virtualenv
python -m virtualenv env
env/Scripts/activate
```
Então instale as dependências do projeto através do gerenciador de pacotes poetry:
```
pip install poetry
poetry install
```

**Variáveis de ambiente** <br>
Para aplicar variáveis para sua máquina, crie um arquivo chamando ".env" e defina as configurações locais. <br>

**Configurações pessoais** <br>
Para criar configurações pessoais, crie uma pasta chamada "instance", e dentro um arquivo "config.py" para armazenar configurações pessoais. As configurações especificadas nesses arquivos não serão compartilhadas.


----------
<h3>Rodando o projeto</h3>

**Configurando seu usuário da base de dados**<br>

A base de dados está configurada para se conectar ao usuário "root", sem senha em seu MySQL.
Para alterar essa configuração, no arquivo de configurações locais "instance/config.py" determine as variáveis:
```
DB_USUARIO = "seu_usuario"
DB_SENHA = "sua_senha"
```
O app oferece como suporte a criação de um banco de dados exemplo e também sua deleção. O banco de dados está configurado para se conectar ao usuário *root*, sem senha em seu servidor MySQL.<br><br>
Para criar e deletar a base de dados na máquina local, execute os comandos:<br>
`flask --app banco init-db`<br>
`flask --app banco drop-db`
<br>
Após instalar as dependências, o projeto está pronto pra ser rodado na sua máquina. Basta executar o comando:
```
flask --app banco run
```

<small>*Para evitar especificar "--app banco" ao executar os comandos, determine a variável **FLASK_APP="banco"** no seu arquivo .env*</small><br><br> 