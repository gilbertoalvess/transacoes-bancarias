# banco.py

from typing import List, Dict

# Banco de dados simulado com contas bancárias
contas_bancarias_db: Dict[int, float] = {
    1: 1000.50,  # Conta do usuário 1 com saldo inicial
    2: 5000.00   # Conta do usuário 2 com saldo inicial
}

def listar_contas() -> List[Dict]:
    return [{"usuario_id": usuario_id, "saldo": saldo} for usuario_id, saldo in contas_bancarias_db.items()]

def transferencia(usuario_origem: int, usuario_destino: int, valor: float) -> Dict:
    if usuario_origem not in contas_bancarias_db or usuario_destino not in contas_bancarias_db:
        return {"erro": "Usuário não encontrado"}
    
    if contas_bancarias_db[usuario_origem] < valor:
        return {"erro": "Saldo insuficiente"}

    contas_bancarias_db[usuario_origem] -= valor
    contas_bancarias_db[usuario_destino] += valor
    return {"mensagem": f"Transferência de {valor} realizada com sucesso!"}

def verificar_saldo(usuario_id: int) -> Dict:
    if usuario_id not in contas_bancarias_db:
        return {"erro": "Usuário não encontrado"}
    
    return {"usuario_id": usuario_id, "saldo": contas_bancarias_db[usuario_id]}
