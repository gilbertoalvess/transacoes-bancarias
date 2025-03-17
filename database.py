from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./transacoes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criar a base para os modelos
Base = declarative_base()

# Criar a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

