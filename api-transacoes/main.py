from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel, validator
from models import Transacao
from database import SessionLocal, engine, Base
from typing import Dict
import logging

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ------------------- MIDDLEWARE GLOBAL PARA ERROS -------------------
@app.middleware("http")
async def middleware_tratamento_erros(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_error:
        return JSONResponse(
            status_code=http_error.status_code,
            content={"erro": http_error.detail}
        )
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro interno no servidor. Por favor, tente novamente mais tarde."}
        )

# ------------------- CONEXÃO COM O BANCO -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- MODELO DE TRANSAÇÃO (Pydantic) -------------------
class TransacaoCreate(BaseModel):
    tipo: str
    valor: float
    usuario_id: int

    @validator('tipo')
    def validar_tipo(cls, v):
        if v not in ['deposito', 'retirada']:
            raise ValueError('O tipo de transação deve ser "deposito" ou "retirada"')
        return v

    @validator('valor')
    def validar_valor(cls, v):
        if v <= 0:
            raise ValueError('O valor precisa ser maior que zero.')
        return v

# ------------------- ENDPOINTS DE TRANSAÇÃO -------------------
@app.post("/transacoes")
def criar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db)):
    try:
        db_transacao = Transacao(tipo=transacao.tipo,
                                 valor=transacao.valor,
                                 usuario_id=transacao.usuario_id)
        db.add(db_transacao)
        db.commit()
        db.refresh(db_transacao)
        return {"mensagem": "Transação criada com sucesso!", "transacao": db_transacao}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade no banco de dados.")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Erro no banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados.")

@app.get("/transacoes")
def listar_transacoes(db: Session = Depends(get_db)):
    transacoes = db.query(Transacao).all()
    return {"mensagem": "Todas as transações", "transacoes": transacoes}

@app.get("/transacoes/{usuario_id}")
def transacoes_usuario(usuario_id: str, db: Session = Depends(get_db)):
    if not usuario_id.isdigit():
        raise HTTPException(status_code=400, detail="O ID do usuário deve ser um número inteiro válido.")

    usuario_id = int(usuario_id)
    transacoes_usuario = db.query(Transacao).filter(Transacao.usuario_id == usuario_id).all()

    transacoes_formatadas = [
        {"id": t.id, "tipo": t.tipo, "valor": t.valor, "usuario_id": t.usuario_id}
        for t in transacoes_usuario
    ]

    return {"mensagem": f"Transações do usuário {usuario_id}", "transacoes": transacoes_formatadas}

# ------------------- MODELO DE CONTAS BANCÁRIAS (Simulação) -------------------
contas_bancarias_db: Dict[int, float] = {
    1: 1000.50,
    2: 5000.00
}

@app.get("/contas")
def get_contas():
    return [{"usuario_id": uid, "saldo": saldo} for uid, saldo in contas_bancarias_db.items()]

@app.get("/saldo/{usuario_id}")
def get_saldo(usuario_id: int):
    if usuario_id not in contas_bancarias_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {"usuario_id": usuario_id, "saldo": contas_bancarias_db[usuario_id]}

@app.post("/transferencia")
def post_transferencia(usuario_origem: int, usuario_destino: int, valor: float):
    if usuario_origem not in contas_bancarias_db or usuario_destino not in contas_bancarias_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if contas_bancarias_db[usuario_origem] < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar a transferência.")
    contas_bancarias_db[usuario_origem] -= valor
    contas_bancarias_db[usuario_destino] += valor
    return {"mensagem": f"Transferência de {valor} realizada com sucesso!"}

# ------------------- ENDPOINTS DE DEPÓSITO E RETIRADA -------------------
@app.post("/deposito")
def deposito(usuario_id: int, valor: float, db: Session = Depends(get_db)):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="O valor do depósito precisa ser maior que zero.")
    if usuario_id not in contas_bancarias_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    contas_bancarias_db[usuario_id] += valor
    return {"mensagem": f"Depósito de {valor} realizado com sucesso para o usuário {usuario_id}."}

@app.post("/retirada")
def retirada(usuario_id: int, valor: float, db: Session = Depends(get_db)):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="O valor da retirada precisa ser maior que zero.")
    if usuario_id not in contas_bancarias_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if contas_bancarias_db[usuario_id] < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar a retirada.")
    contas_bancarias_db[usuario_id] -= valor
    return {"mensagem": f"Retirada de {valor} realizada com sucesso para o usuário {usuario_id}."}
