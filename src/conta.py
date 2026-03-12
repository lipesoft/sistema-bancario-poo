from typing import Optional, TYPE_CHECKING
from src.historico import Historico

if TYPE_CHECKING:
    from src.cliente import Cliente


class Conta:
    """Classe base para contas bancárias."""
    
    def __init__(self, numero: int, cliente: 'Cliente'):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self) -> float:
        """Retorna o saldo atual da conta."""
        return self._saldo
    
    @property
    def numero(self) -> int:
        """Retorna o número da conta."""
        return self._numero
    
    @property
    def agencia(self) -> str:
        """Retorna a agência da conta."""
        return self._agencia
    
    @property
    def cliente(self) -> 'Cliente':
        """Retorna o cliente titular da conta."""
        return self._cliente
    
    @property
    def historico(self) -> Historico:
        """Retorna o histórico da conta."""
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        """
        Método de fábrica para criar uma nova conta.
        
        Args:
            cliente: Cliente titular da conta
            numero: Número da conta
        
        Returns:
            Nova instância de Conta
        """
        conta = cls(numero, cliente)
        cliente.adicionar_conta(conta)
        return conta
    
    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta.
        
        Args:
            valor: Valor a ser sacado
        
        Returns:
            True se o saque foi bem-sucedido, False caso contrário
        """
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        
        self._saldo -= valor
        return True
    
    def depositar(self, valor: float) -> bool:
        """
        Realiza um depósito na conta.
        
        Args:
            valor: Valor a ser depositado
        
        Returns:
            True se o depósito foi bem-sucedido, False caso contrário
        """
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        self._saldo += valor
        return True
    
    def __str__(self) -> str:
        return f"Agência: {self._agencia} | Conta: {self._numero} | Saldo: R$ {self._saldo:.2f}"


class ContaCorrente(Conta):
    """Classe concreta para contas correntes com limites específicos."""
    
    def __init__(self, numero: int, cliente: 'Cliente', 
                 limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    @property
    def limite(self) -> float:
        """Retorna o limite de saque por operação."""
        return self._limite
    
    @property
    def limite_saques(self) -> int:
        """Retorna o limite diário de saques."""
        return self._limite_saques
    
    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta corrente com validações adicionais.
        
        Args:
            valor: Valor a ser sacado
        
        Returns:
            True se o saque foi bem-sucedido, False caso contrário
        """
        # Conta número de saques no dia atual
        from datetime import datetime
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        numero_saques_hoje = len([
            t for t in self.historico.transacoes 
            if t['tipo'] == 'Saque' and t['data'].startswith(hoje)
        ])
        
        if numero_saques_hoje >= self._limite_saques:
            print("Operação falhou! Número máximo de saques diários excedido.")
            return False
        
        if valor > self._limite:
            print(f"Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
            return False
        
        return super().sacar(valor)
    
    def __str__(self) -> str:
        return (f"Conta Corrente | Ag: {self._agencia} | "
                f"Nº: {self._numero} | Saldo: R$ {self._saldo:.2f} | "
                f"Limite: R$ {self._limite:.2f}")