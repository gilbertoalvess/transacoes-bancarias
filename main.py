from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from datetime import datetime, timedelta
from auth import criar_token_jwt, verificar_token_jwt

app = FastAPI()

# 🔹 Definição do cabeçalho de autenticação
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

# 🔹 Simulação de banco de usuários
fake_users_db = {
    "usuario1": {"username": "usuario1", "password": "senha123"},
    "usuario2": {"username": "usuario2", "password": "senha456"}
}

# 🔹 Simulação de banco de dados de contas bancárias
contas_bancarias_db = {
    1: {"usuario": "usuario1", "saldo": 1000.0, "transacoes": []},
    2: {"usuario": "usuario2", "saldo": 500.0, "transacoes": []}
}

@app.post("/login")
def login(username: str, password: str):
    """Autentica o usuário e retorna um token JWT."""
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    token_expira = timedelta(minutes=30)
    access_token = criar_token_jwt({"sub": username}, expira_em=token_expira)

    return {"access_token": access_token, "token_type": "bearer"}

def autenticar_usuario(api_key: str = Security(api_key_header)):
    """Valida o token JWT enviado no cabeçalho Authorization."""
    if not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")

    token = api_key.split(" ")[1]
    return verificar_token_jwt(token)

@app.get("/saldo")
def saldo(usuario: str = Depends(autenticar_usuario)):
    """Retorna o saldo do usuário autenticado"""
    for conta in contas_bancarias_db.values():
        if conta["usuario"] == usuario:
            return {"usuario": usuario, "saldo": conta["saldo"]}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.post("/retirada")
def retirada(valor: float, usuario: str = Depends(autenticar_usuario)):
    """Realiza uma retirada do saldo do usuário autenticado"""
    for conta in contas_bancarias_db.values():
        if conta["usuario"] == usuario:
            if conta["saldo"] >= valor:
                conta["saldo"] -= valor
                transacao = {
                    "id": len(conta["transacoes"]) + 1,
                    "data": datetime.now().isoformat(),
                    "tipo": "retirada",
                    "valor": valor
                }
                conta["transacoes"].append(transacao)
                return {"mensagem": f"Retirada de {valor} realizada com sucesso."}
            else:
                raise HTTPException(status_code=400, detail="Saldo insuficiente")
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/extrato")
def extrato(usuario: str = Depends(autenticar_usuario)):
    """Retorna o extrato bancário do usuário autenticado"""
    for conta in contas_bancarias_db.values():
        if conta["usuario"] == usuario:
            return {
                "usuario": usuario,
                "extrato": conta["transacoes"],
                "saldo_atual": conta["saldo"]
            }
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# 🔹 Endpoint para transferência entre usuários
@app.post("/transferencia")
def transferencia(destinatario: str, valor: float, usuario: str = Depends(autenticar_usuario)):
    """Realiza uma transferência para outro usuário"""
    if destinatario not in [conta["usuario"] for conta in contas_bancarias_db.values()]:
        raise HTTPException(status_code=404, detail="Destinatário não encontrado")

    conta_origem = next((conta for conta in contas_bancarias_db.values() if conta["usuario"] == usuario), None)
    conta_destino = next((conta for conta in contas_bancarias_db.values() if conta["usuario"] == destinatario), None)

    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if conta_origem["saldo"] < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    # Realiza a transferência
    conta_origem["saldo"] -= valor
    conta_destino["saldo"] += valor

    # Registra a transação
    transacao_origem = {
        "id": len(conta_origem["transacoes"]) + 1,
        "data": datetime.now().isoformat(),
        "tipo": "transferência enviada",
        "valor": valor,
        "para": destinatario
    }
    conta_origem["transacoes"].append(transacao_origem)

    transacao_destino = {
        "id": len(conta_destino["transacoes"]) + 1,
        "data": datetime.now().isoformat(),
        "tipo": "transferência recebida",
        "valor": valor,
        "de": usuario
    }
    conta_destino["transacoes"].append(transacao_destino)

    return {"mensagem": f"Transferência de {valor} para {destinatario} realizada com sucesso."}

# 🔹 Endpoint para depositar dinheiro
@app.post("/deposito")
def deposito(valor: float, usuario: str = Depends(autenticar_usuario)):
    """Realiza um depósito na conta do usuário autenticado"""
    for conta in contas_bancarias_db.values():
        if conta["usuario"] == usuario:
            conta["saldo"] += valor
            transacao = {
                "id": len(conta["transacoes"]) + 1,
                "data": datetime.now().isoformat(),
                "tipo": "depósito",
                "valor": valor
            }
            conta["transacoes"].append(transacao)
            return {"mensagem": f"Depósito de {valor} realizado com sucesso."}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# 🔹 Adiciona a autenticação no Swagger UI
@app.on_event("startup")
def customize_openapi():
    if not app.openapi_schema:
        return
    openapi_schema = app.openapi()
    openapi_schema["components"] = {
        "securitySchemes": {
            "APIKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            }
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"APIKeyAuth": []}]
    app.openapi_schema = openapi_schema
