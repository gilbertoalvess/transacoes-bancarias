from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# @app.get("/")
# def home():
#    return {"mensagem": "Bem-vindo à API de Transações Bancárias"}

# ------------------- MODELO DE TRANSAÇÃO -------------------

class Transacao(BaseModel):
    tipo: str  # 'deposito' ou 'retirada'
    valor: float
    usuario_id: int

# Lista para armazenar as transações
transacoes_db = []

# Endpoint para criar uma transação
@app.post("/transacoes")
def criar_transacao(transacao: Transacao):
    transacoes_db.append(transacao)
    return {"mensagem": "Transação criada com sucesso!", "transacao": transacao}

# Endpoint para listar todas as transações
@app.get("/transacoes")
def listar_transacoes():
    return {"mensagem": "Todas as transações", "transacoes": transacoes_db}

# Endpoint para visualizar as transações de um usuário específico
@app.get("/transacoes/{usuario_id}")
def transacoes_usuario(usuario_id: int):
    transacoes_usuario = [t for t in transacoes_db if t.usuario_id == usuario_id]
    return {"mensagem": f"Transações do usuário {usuario_id}", "transacoes": transacoes_usuario}

# ------------------- MODELO DE CONTAS BANCÁRIAS -------------------
# Simulação de contas bancárias (Banco de dados fake)
contas_bancarias_db: Dict[int, float] = {
    1: 1000.50,  # Conta do usuário 1 com saldo inicial
    2: 5000.00   # Conta do usuário 2 com saldo inicial
}

# Endpoint para listar contas bancárias
@app.get("/contas")
def get_contas():
    return [{"usuario_id": usuario_id, "saldo": saldo} for usuario_id, saldo in contas_bancarias_db.items()]

# Endpoint para verificar saldo de um usuário
@app.get("/saldo/{usuario_id}")
def get_saldo(usuario_id: int):
    if usuario_id not in contas_bancarias_db:
        return {"erro": "Usuário não encontrado"}
    return {"usuario_id": usuario_id, "saldo": contas_bancarias_db[usuario_id]}

# Endpoint para realizar transferências
@app.post("/transferencia")
def post_transferencia(usuario_origem: int, usuario_destino: int, valor: float):
    if usuario_origem not in contas_bancarias_db or usuario_destino not in contas_bancarias_db:
        return {"erro": "Usuário não encontrado"}
    
    if contas_bancarias_db[usuario_origem] < valor:
        return {"erro": "Saldo insuficiente"}

    contas_bancarias_db[usuario_origem] -= valor
    contas_bancarias_db[usuario_destino] += valor
    return {"mensagem": f"Transferência de {valor} realizada com sucesso!"}



