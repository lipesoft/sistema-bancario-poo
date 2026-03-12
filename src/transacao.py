from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Evita import circular
if TYPE_CHECKING:
    from src.conta import Conta


class Transacao(ABC):
    """Classe abstrata que define o contrato para todas as transações."""
    
    @property
    @abstractmethod
    def valor(self) -> float:
        """Propriedade abstrata que deve retornar o valor da transação."""
        pass
    
    @abstractmethod
    def registrar(self, conta: 'Conta') -> None:
        """
        Registra a transação em uma conta.
        
        Args:
            conta: Conta onde a transação será registrada
        """
        pass


class Deposito(Transacao):
    """Classe concreta que representa uma operação de depósito."""
    
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: 'Conta') -> None:
        """
        Registra um depósito na conta.
        
        Args:
            conta: Conta onde o depósito será realizado
        """
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso!")
    
    def __str__(self) -> str:
        return f"Depósito: R$ {self.valor:.2f}"


class Saque(Transacao):
    """Classe concreta que representa uma operação de saque."""
    
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: 'Conta') -> None:
        """
        Registra um saque na conta.
        
        Args:
            conta: Conta onde o saque será realizado
        """
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso!")
    
    def __str__(self) -> str:
        return f"Saque: R$ {self.valor:.2f}"