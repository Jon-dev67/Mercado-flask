Mercado Flask

Este é um projeto de exemplo utilizando Flask para criar uma aplicação web de cadastro de usuários e gerenciamento de itens. A aplicação utiliza um banco de dados SQLite para armazenar informações e inclui funcionalidades de autenticação, cadastro de usuários, exibição de produtos e login.


---

Tecnologias Utilizadas

Flask: Framework web para Python.

Flask-SQLAlchemy: Integração com o banco de dados SQLite.

Flask-WTF: Criação e validação de formulários.

Flask-Bcrypt: Criptografia de senhas.

Flask-Login: Gerenciamento de sessões de usuários.

Bootstrap: Para estilização das páginas HTML.



---

Funcionalidades

1. Cadastro de Usuários

Validação para evitar duplicação de usuários, e-mails e senhas.

Armazenamento seguro de senhas utilizando hash com Flask-Bcrypt.


2. Login de Usuários

Validação de credenciais (usuário e senha).

Gerenciamento de sessão com Flask-Login.


3. Exibição de Produtos

Recuperação e exibição de itens cadastrados no banco de dados.



---

Estrutura do Banco de Dados

Tabela User

Tabela Item


---

Rotas da Aplicação

Rota Principal (Home)

GET /: Renderiza a página inicial (home.html).


Produtos

GET /produtos: Exibe os produtos cadastrados no banco de dados.


Cadastro

GET, POST /cadastro: Página para cadastro de novos usuários com validação de dados.


Login

GET, POST /login: Página para login de usuários já cadastrados.



---

Como Executar o Projeto

1. Clone o repositório:

git clone git@github.com:jon-dev/Mercado-flask.git
cd Mercado-flask


2. Instale as dependências:

pip install -r requirements.txt


3. Configure o banco de dados: O banco de dados será criado automaticamente ao iniciar a aplicação.


4. Execute a aplicação:

python app.py


5. Acesse a aplicação: Abra o navegador e acesse http://127.0.0.1:5000.




---

Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.


---

Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.


---
