# 📌 API de Transações Bancárias

Bem-vindo ao projeto **API de Transações Bancárias**! Esta é uma API desenvolvida com **FastAPI** e **SQLite**, permitindo realizar operações bancárias como depósitos, retiradas e transferências entre usuários.

---

## 🚀 Tecnologias Utilizadas
- **Python** (FastAPI)
- **SQLite** (Banco de Dados)
- **SQLAlchemy** (ORM para banco de dados)
- **Uvicorn** (Servidor ASGI)

---

## ⚙️ Como Rodar o Projeto

### 🔹 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 🔹 2. Criar um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 🔹 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 🔹 4. Rodar a API
```bash
uvicorn main:app --reload
```

A API ficará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Como Testar a API
Acesse a documentação interativa do FastAPI:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 📌 Exemplo de Requisição - Criar uma Transação (POST `/transacoes`)
```json
{
  "tipo": "deposito",
  "valor": 100.0,
  "usuario_id": 1
}
```

### 📌 Exemplo de Resposta
```json
{
  "mensagem": "Transação criada com sucesso!",
  "transacao": {
    "id": 1,
    "tipo": "deposito",
    "valor": 100.0,
    "usuario_id": 1
  }
}
```

---

## 📌 Endpoints Disponíveis
| Método | Rota | Descrição |
|---------|------|-------------|
| **POST** | `/transacoes` | Criar uma transação |
| **GET** | `/transacoes` | Listar todas as transações |
| **GET** | `/transacoes/{usuario_id}` | Listar transações de um usuário |
| **POST** | `/deposito` | Realizar um depósito |
| **POST** | `/retirada` | Realizar uma retirada |
| **GET** | `/saldo/{usuario_id}` | Consultar saldo do usuário |
| **POST** | `/transferencia` | Realizar transferência entre contas |

---

## 📌 Autor
Projeto desenvolvido por Gilberto Alves. Entre em contato:
- 💼 [LinkedIn](https://www.linkedin.com/in/gilberto-alves-silva-desenvolvedor-software)
- 📧 ga220585@gmail.com

