from datetime import datetime
from typing import List, Dict, Any


class Historico:
    """Classe responsável por armazenar o histórico de transações de uma conta."""
    
    def __init__(self):
        self._transacoes: List[Dict[str, Any]] = []
    
    @property
    def transacoes(self) -> List[Dict[str, Any]]:
        """Retorna a lista de transações."""
        return self._transacoes.copy()  # Retorna cópia para proteger o encapsulamento
    
    def adicionar_transacao(self, transacao: 'Transacao') -> None:
        """
        Adiciona uma transação ao histórico.
        
        Args:
            transacao: Objeto transacao (Deposito ou Saque)
        """
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })
    
    def gerar_extrato(self) -> str:
        """Gera um extrato formatado com todas as transações."""
        if not self._transacoes:
            return "Não foram realizadas movimentações."
        
        extrato = []
        for transacao in self._transacoes:
            extrato.append(
                f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}"
            )
        
        return "\n".join(extrato)
    
    def __len__(self) -> int:
        """Retorna o número de transações no histórico."""
        return len(self._transacoes)
    
    def __str__(self) -> str:
        """Representação em string do histórico."""
        return f"Histórico com {len(self)} transações"