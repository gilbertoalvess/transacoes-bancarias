from sqlalchemy import Column, Integer, String, Float
from database import Base

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)
    valor = Column(Float)
    usuario_id = Column(Integer, index=True)
