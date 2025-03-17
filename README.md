# 💰 Transações Bancárias - API em FastAPI

Este projeto é uma API de transações bancárias desenvolvida com **FastAPI**, permitindo operações como login, consulta de saldo, retiradas, depósitos e transferências entre contas.  

## 🚀 Tecnologias Utilizadas
- **Python 3.10+**
- **FastAPI**
- **SQLite** (Banco de Dados)
- **JWT** (Autenticação)
- **Uvicorn** (Servidor ASGI)
- **Git/GitHub** (Controle de Versão)

## 🔧 Como Rodar o Projeto Localmente

### 1️⃣ Clone o Repositório
```sh
git clone https://github.com/gilbertoalvess/transacoes-bancarias.git
cd transacoes-bancarias/api-transacoes
```

### 2️⃣ Crie um Ambiente Virtual e Ative
```sh
python -m venv venv
# Ativar no Windows:
venv\Scripts\activate
# Ativar no Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Instale as Dependências
```sh
pip install -r requirements.txt
```

### 4️⃣ Inicie a API
```sh
uvicorn main:app --reload
```

A API estará disponível em:  
📌 **http://127.0.0.1:8000**  

A documentação interativa do Swagger pode ser acessada em:  
📌 **http://127.0.0.1:8000/docs**

## 🔑 Autenticação
A API utiliza **JWT** para autenticação.  
Para obter um token:

1. Faça uma requisição **POST** para `/login` com `username` e `password` válidos.
2. Utilize o token gerado para acessar os endpoints protegidos (como `/saldo`, `/retirada`, etc.).

## 📌 Endpoints Disponíveis

| Método | Rota            | Descrição |
|---------|----------------|-------------|
| **POST**   | `/login`       | Autentica o usuário e gera um token JWT |
| **GET**    | `/saldo`       | Consulta o saldo do usuário autenticado |
| **POST**   | `/retirada`    | Realiza uma retirada da conta do usuário |
| **GET**    | `/extrato`     | Consulta o extrato bancário |
| **POST**   | `/transferencia` | Transfere saldo entre contas |
| **POST**   | `/deposito`    | Realiza um depósito na conta |

## 📢 Contato

👨‍💻 **Gilberto Alves**  
📧 **E-mail:** ga220585@gmail.com  
🌟 **LinkedIn:** [linkedin.com/in/gilberto-alves-silva-desenvolvedor-software](https://linkedin.com/in/gilberto-alves-silva-desenvolvedor-software)