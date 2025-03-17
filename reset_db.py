from database import SessionLocal
from models import Transacao

db = SessionLocal()

# Apaga todas as transações
db.query(Transacao).delete()
db.commit()

print("Banco de dados resetado com sucesso!")
