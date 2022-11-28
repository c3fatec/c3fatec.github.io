<div>

<img src="https://i.ibb.co/QDpNydM/APRESENTA-O-C3-1-SPRINT-Capa-para-Facebook.jpg" alt="APRESENTA-O-C3-1-SPRINT-Capa-para-Facebook" border="0" />

</div>
<br id="topo">
<p align="center">
    <a href="#sobre">Sobre</a>  |  
    <a href="#sprints">Sprints</a>  | 
    <a href="#backlogs">Product Backlog</a>  |  
    <a href="#demo">Demonstração</a>  |    
    <a href="#tecnologias">Tecnologias</a>  |  
    <a href="#equipe">Equipe</a> |
    <a href="#instru">Instruções</a>
</p>

---

<h2 id='sobre'>Sobre</h2>
Esse repositório contém o primeiro projeto API dos estudantes do primeiro semestre 2022/2 de DSM da Fatec de São José dos Campos. O projeto propõe a criação de uma aplicação que simule um banco digital, com funcionalidades para criação e manutenção de uma conta de usuário, gerenciamento interno e display responsivo para web.

---

<!-- ## :date: Sprints -->

<h2 id='sprints'>Sprints</h2>

| Sprint | Data Final |    Status    |
| :----: | :--------: | :----------: |
|   01   | 18/09/2022 | ✔️ Concluída |
|   02   | 19/10/2022 | ✔️ Concluída |
|   03   | 06/11/2022 | ✔️ Concluída |
|   04   | 27/11/2022 | ✔️ Concluída |

[![Generic badge](https://img.shields.io/badge/STATUS%20DO%20PROJETO-CONCLU%C3%8DDO-green)](https://shields.io/)
---

<!-- ## :open_file_folder:Product Backlog -->

<h2 id='backlogs'>Product Backlog</h2>

<img src="https://i.ibb.co/QkjxWmN/backlog-total.jpg" alt="Product-Backlog" border="0">

<h5>1º Sprint -  <a href="https://i.ibb.co/TgW062T/pb1.png">Clique aqui</a>

<h5>2º Sprint -  <a href="https://i.ibb.co/M6n9cFr/Product-Backlog.jpg">Clique aqui</a>

<h5>3º Sprint -  <a href="https://i.ibb.co/HHS62zn/back-log-sprint-3.jpg">Clique aqui</a>

---

<h2 name='tecnologias'>Tecnologias Utilizadas</h2>

<img src="https://i.ibb.co/WPH798M/tec3.jpg" alt="Tecnologiasc3" border="0">



---

<h2 id='demo'>Demonstração</h2>


![](./banco/static/video/Xbank1.gif)
<!-- <h5>1º Sprint -  <a href="https://www.loom.com/share/40d65d6ff2574e0586003a2e2f3d7e57">Clique aqui</a>
<h5>2º Sprint -  <a href="https://www.loom.com/share/40d65d6ff2574e0586003a2e2f3d7e57">Clique aqui</a>
<h5>3º Sprint -  <a href="https://www.loom.com/share/40d65d6ff2574e0586003a2e2f3d7e57">Clique aqui</a>
 -->
---

<h2 id='equipe'>Equipe</h2>



| Função        | Nome                                                                                                                                                                                         |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Product Owner | [![GitHub](https://i.stack.imgur.com/tskMh.png)](https://github.com/dmssjk/) [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/) Daniel Machado dos Santos         |
| Scrum Master  | [![GitHub](https://i.stack.imgur.com/tskMh.png)](https://github.com/dosantos-ogabriel) [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/) Gabriel Oliveira Santos |
| Dev Team      | [![GitHub](https://i.stack.imgur.com/tskMh.png)](https://github.com/IvanSuiyama) [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/) Ivan Suiyma                   |
| Dev Team      | [![GitHub](https://i.stack.imgur.com/tskMh.png)](https://github.com/JacklesKerley) [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/) Jackles Kerley              |
| Dev Team      | [![GitHub](https://i.stack.imgur.com/tskMh.png)](https://github.com/) [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/) Claudinei Paulista                       |

---

<h2 id='instru'>Instruções</h2>

**Instalando o projeto**

**As instruções assumem um computador windows com python 3.10 já instalado**

Para rodar o projeto em sua máquina, inicie um ambiente virtual:

```
py -m venv env
env/Scripts/activate
```

Então instale as dependências do projeto:

```
pip install -r requirements.txt
```


**Variáveis de ambiente** <br>
Para aplicar variáveis para sua máquina, crie um arquivo chamando ".env" e defina as configurações locais. <br>

**Configurações pessoais** <br>
Para criar configurações pessoais, crie uma pasta chamada "instance", e dentro um arquivo "config.py" para armazenar configurações pessoais. As configurações especificadas nesses arquivos não serão compartilhadas.

---

<h3>Rodando o Projeto</h3>

**Configurando seu usuário da base de dados**<br>


O app oferece como suporte a criação de um banco de dados exemplo e também sua deleção. O banco de dados está configurado para se conectar ao usuário _root_, sem senha em seu servidor MySQL.<br><br>
Para alterar essa configuração, no arquivo de configurações locais "instance/config.py" determine as variáveis:

```
DB_USUARIO = "seu_usuario"
DB_SENHA = "sua_senha"
```

Para criar e deletar a base de dados na máquina local, execute os comandos:<br>

```
$ flask --app banco init-db

$ flask --app banco drop-db
```

Após instalar as dependências, o projeto está pronto pra ser rodado na sua máquina. Basta executar o comando:

```
$ flask --app banco run
```

<small>_Para evitar especificar "--app banco" ao executar os comandos, determine a variável **FLASK_APP="banco"** no seu arquivo .env_</small><br><br>

---

<h3>Acessando o Sistema</h3>

**Acesso de Gerente Geral**<br>

localhost:5000/admin

**Login**<br>
**Matricula:** 1  
**Senha:** gerente

**Acesso de gerentes de agência**

**Login**<br>
**Matricula:** 9
**Senha:** daniel

**Login**<br>
**Matricula:** 88888
**Senha:** jackles

**Acesso de clientes exemplo**

**Login**<br>
_conta poupança_ <br>
**Número da conta:** 10000  
**Agência:** 1
**Senha:** cliente

**Login**<br>
_conta corrente_ <br>
**Número da conta:** 20000  
**Agência:** 2
**Senha:** cliente

**Ativando o modo de volta para o futuro**<br>

Para avançar ou voltar a data do sistema utilize os comandos abaixo.

```
$ flask change-time  (data = atual)

$ flask change-time --time=2023-11-25 (data desejada no formato YYYY-mm-dd)
```

Para ativar as taxas de juros após ter alterado a data do sistema utilize o comando.

```
$ flask tax
```
---