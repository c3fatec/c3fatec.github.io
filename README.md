### c3fatec.github.io
# API da turma de DSM da equipe C3

## Rodando o projeto
Crie um ambiente virtual:

```
pip install virtualenv
python -m virtualenv env
env/Scripts/activate
```

Instale as dependências do projeto:

`pip install -r requirements.txt`

Para rodar o app na máquina local:

`flask run`

## Banco de dados
O banco de dados está configurado para se conectar ao usuário *root*, sem senha.

Para criar a base de dados na máquina local, rodar o comando:

`flask init-db`
Para deleter a base de dados:

`flask drop-db`