# **Fintrack API - Documentação**

---

```plaintext
src/
├── fintrack_api/
│   ├── api.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models/
│   │   ├── TokenModels.py
│   │   └── userModels.py
│   ├── routes/
│   │   ├── add_router.py
│   │   ├── delete_router.py
│   │   ├── update_router.py
│   │   ├── user_router.py
│   │   └── visualization_router.py
│   ├── services/
│   │   ├── CRUD/
│   │   │   ├── create.py
│   │   │   ├── read.py
│   │   │   ├── update.py
│   │   │   └── delete.py
│   │   └── db/
│   │       └── sql_connection.py
│   └── utils/
│       ├── fintrack_api_utils.py
│       └── api.py
└── main.py

```

---

## **Modelos de Dados**

### Localização: `src/fintrack_api/models`

Define modelos de dados usando Pydantic para estruturar e validar dados de tokens e usuários.

- **`Token`** (`TokenModels.py`): 
  - Modelo de token de acesso com os atributos:
    - `access_token` (str): Token propriamente dito.
    - `token_type` (str): Tipo do token, como "bearer".

- **`TokenData`** (`TokenModels.py`): 
  - Dados do token, contendo:
    - `user_id` (Union[str, None]): Identificação do usuário, opcional.

- **`UserOut`** (`userModels.py`): 
  - Dados de usuário para exibição, incluindo:
    - `name` (str): Nome.
    - `email` (str): Email.

- **`UserIn`** (`userModels.py`): 
  - Extende `UserOut` para incluir:
    - `password` (str): Senha, usada no registro de novos usuários.

- **`UserInDB`** (`userModels.py`): 
  - Dados do usuário no banco de dados, incluindo:
    - `name` (str): Nome.
    - `email` (str): Email.
    - `password` (str): Senha com hash.

---

## **Serviços CRUD**

### Localização: `src/fintrack_api/services/CRUD`

Define operações CRUD para gerenciar usuários e itens no banco de dados.

- **Create** (`create.py`):
  - **`create_user`**: Registra um novo usuário.
  - **`add_item_to_db`**: Insere um item em uma tabela específica (receita, despesa, alerta ou lembrete) usando o modelo `AddItem`.

- **Read** (`read.py`):
  - **`get_all_users`**: Recupera todos os usuários.
  - **`get_user_by_email_for_auth`**: Busca usuário por email para autenticação.
  - **`get_all_items_from_db`**: Recupera todos os itens de uma tabela, opcionalmente filtrados por email.

- **Update** (`update.py`):
  - Funções para atualizar entradas específicas (receita, despesa, alerta e lembrete) com base no email, usando `update_item`.

- **Delete** (`delete.py`):
  - Funções para deletar entradas específicas (receita, despesa, alerta e lembrete) com base no email, usando `delete_item`.

---

## **Conexão com Banco de Dados**

### Localização: `src/fintrack_api/services/db/sql_connection.py`

Define a conexão com o banco de dados PostgreSQL usando variáveis de ambiente.

- **`connect`**:
  - Estabelece uma conexão com o banco de dados, utilizando credenciais e informações do arquivo `.env`.

---

## **Utilitários**

### Localização: `src/fintrack_api/utils/frintrack_api_utils.py`

Funções auxiliares para operações de segurança e validação.

- **`get_password_hash`**: Gera o hash da senha com bcrypt.
- **`verify_password`**: Verifica se uma senha corresponde ao hash armazenado.
- **`validate_password_strength`**: Valida se a senha tem pelo menos 6 caracteres.
- **`validate_email_format`**: Verifica o formato do email, permitindo domínios `.com` e `.br`.

---

## **Rotas da API**

### Localização: `src/fintrack_api/api.py`

Define endpoints da API para gerenciamento de usuários e dados financeiros.

### **User Routes**

- **`/login`** (POST): Autentica um usuário e retorna um token JWT.
- **`/user/register`** (POST): Registra um novo usuário.

### **Add Routes**

- **`/add/revenue`**, **`/add/expenditure`**, **`/add/alert`**, **`/add/reminder`** (POST): 
  - Adiciona entradas ao banco de dados para receita, despesa, alerta ou lembrete.

### **Visualization Routes**

- **`/visualization/revenue`**, **`/visualization/expenditure`**, **`/visualization/alert`**, **`/visualization/reminder`** (GET): 
  - Recupera dados com filtro opcional por email.

### **Update Routes**

- **`/update/revenue`**, **`/update/expenditure`**, **`/update/alert`**, **`/update/reminder`** (PUT): 
  - Atualiza entradas específicas com base no email.

### **Delete Routes**

- **`/delete/revenue`**, **`/delete/expenditure`**, **`/delete/alert`**, **`/delete/reminder`** (DELETE): 
  - Deleta entradas específicas com base no email.

---

## **Dependências**

### Localização: `src/fintrack_api/dependencies.py`

Fornece funções utilitárias e autenticação com OAuth2 e JWT.

- **`get_api_key`**: Valida a API key nos cabeçalhos da solicitação.
- **`create_access_token`**: Gera um token JWT com expiração opcional.
- **`authenticate_user`**: Autentica um usuário com base em email e senha.
- **`get_current_user`** e **`get_current_user_id`**: Obtêm o usuário autenticado ou seu ID a partir de um token JWT.
