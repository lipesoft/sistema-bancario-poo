from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.conta import Conta
    from src.transacao import Transacao


class Cliente(ABC):
    """Classe abstrata base para todos os clientes do banco."""
    
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas: List['Conta'] = []
    
    @property
    def endereco(self) -> str:
        """Retorna o endereço do cliente."""
        return self._endereco
    
    @property
    def contas(self) -> List['Conta']:
        """Retorna a lista de contas do cliente."""
        return self._contas.copy()  # Retorna cópia para proteger encapsulamento
    
    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao') -> None:
        """
        Realiza uma transação em uma conta específica.
        
        Args:
            conta: Conta onde a transação será realizada
            transacao: Transação a ser executada
        """
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta: 'Conta') -> None:
        """
        Adiciona uma conta ao cliente.
        
        Args:
            conta: Conta a ser adicionada
        """
        self._contas.append(conta)
    
    @abstractmethod
    def identificar(self) -> str:
        """Método abstrato para identificar o cliente."""
        pass
    
    def __str__(self) -> str:
        return f"Cliente com {len(self._contas)} conta(s)"


class PessoaFisica(Cliente):
    """Classe concreta para clientes pessoa física."""
    
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self) -> str:
        """Retorna o CPF do cliente."""
        return self._cpf
    
    @property
    def nome(self) -> str:
        """Retorna o nome do cliente."""
        return self._nome
    
    @property
    def data_nascimento(self) -> date:
        """Retorna a data de nascimento do cliente."""
        return self._data_nascimento
    
    def identificar(self) -> str:
        """Retorna o CPF como identificador do cliente."""
        return self._cpf
    
    def __str__(self) -> str:
        return f"{self._nome} (CPF: {self._cpf})"