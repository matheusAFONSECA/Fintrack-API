### **Fintrack API - Visão Geral da Documentação**

---

### **Modelos (src/fintrack_api/models/userModels.py)**
Define modelos de dados utilizando Pydantic para estruturar e validar dados relacionados aos usuários.

- **`UserOut`**: Representa os dados de um usuário para saída, incluindo `name` (nome), `email`, `phone` (telefone) e `birth` (data de nascimento).

- **`UserIn`**: Extende o `UserOut` com os campos adicionais `cpf` (identificação do usuário) e `password` (senha) para registro de novos usuários.

- **`UserInDB`**: Representa os dados do usuário armazenados no banco de dados, incluindo o `hashed_password` (hash da senha) e `user_id` (ID do usuário).

- **`UserInQuery`**: Permite consultas opcionais de usuários utilizando parâmetros como `name`, `email`, `phone` e `birth`.

---

### **Rotas (src/fintrack_api/routes/userRoutes.py)**
Define os endpoints da API relacionados ao gerenciamento de usuários.

- **`/login`** (POST): Autentica um usuário e retorna um token JWT em caso de sucesso.

- **`/register`** (POST): Registra um novo usuário com os dados fornecidos, incluindo a senha com hash.

- **`/`** (GET): Recupera todos os usuários registrados no sistema.

---

### **Dependências (src/fintrack_api/dependencies.py)**
Fornece funções utilitárias e mecanismos de autenticação usando OAuth2 e JWT.

- **`get_api_key`**: Valida a API key presente nos cabeçalhos da solicitação.

- **`verify_password` / `get_password_hash`**: Verifica e gera o hash das senhas dos usuários para armazenamento seguro.

- **`authenticate_user`**: Autentica um usuário com base em seu e-mail e senha.

- **`create_access_token`**: Gera um token de acesso JWT com um período de expiração opcional.

- **`get_current_user`**: Obtém o usuário atual autenticado com base no token JWT fornecido.

- **`get_current_user_id`**: Extrai o ID do usuário do token JWT.

---