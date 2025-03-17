from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

# Chave secreta para assinar o token JWT
SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expira em 30 minutos

# Simulação de um banco de usuários (pode ser substituído por um banco real)
fake_users_db = {
    "usuario1": {
        "username": "usuario1",
        "password": "senha123"  # Senha fixa apenas para teste
    }
}

# Configuração para autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def criar_token_jwt(dados: dict, expira_em: Optional[timedelta] = None):
    """Gera um token JWT válido."""
    to_encode = dados.copy()
    if expira_em:
        expire = datetime.utcnow() + expira_em
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    token_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def verificar_token_jwt(token: str = Depends(oauth2_scheme)):
    """Verifica se o token JWT é válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
