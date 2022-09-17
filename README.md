## API da turma de DSM da equipe C3 
# Sobre o projeto
Esse repositório contém o primeiro projeto API dos estudantes do primeiro semestre 2022/2 de DSM da Fatec de São José dos Campos. O projeto propõe a criação de uma aplicação que simule um banco digital, com funcionalidades para criação e manutenção de uma conta de usuário, gerenciamento interno e display responsivo para web.

----------
## Tecnologias utilizadas
O projeto foi criado utilizando as seguintes tecnologias:
  - Versionamento: Git (Github)
  - Banco de dados: MySQL
  - Framework web: Flask
----------
## Instalando o projeto
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
## Rodando o projeto <br>
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
