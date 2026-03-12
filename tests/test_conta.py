import pytest
from datetime import date
from src.cliente import PessoaFisica
from src.conta import Conta, ContaCorrente
from src.transacao import Deposito, Saque
from src.historico import Historico


@pytest.fixture
def cliente():
    """Fixture que retorna um cliente para testes."""
    return PessoaFisica(
        cpf="12345678901",
        nome="Cliente Teste",
        data_nascimento=date(1990, 1, 1),
        endereco="Rua Teste, 123"
    )


@pytest.fixture
def conta(cliente):
    """Fixture que retorna uma conta para testes."""
    return Conta(numero=1, cliente=cliente)


@pytest.fixture
def conta_corrente(cliente):
    """Fixture que retorna uma conta corrente para testes."""
    return ContaCorrente(numero=1, cliente=cliente, limite=1000.0, limite_saques=3)


class TestConta:
    """Testes para a classe Conta."""
    
    def test_criar_conta(self, conta, cliente):
        """Testa a criação de uma conta."""
        assert conta.numero == 1
        assert conta.agencia == "0001"
        assert conta.cliente == cliente
        assert conta.saldo == 0.0
        assert isinstance(conta.historico, Historico)
    
    def test_depositar_valor_positivo(self, conta):
        """Testa depósito com valor positivo."""
        resultado = conta.depositar(100.0)
        assert resultado is True
        assert conta.saldo == 100.0
    
    def test_depositar_valor_negativo(self, conta):
        """Testa depósito com valor negativo."""
        resultado = conta.depositar(-50.0)
        assert resultado is False
        assert conta.saldo == 0.0
    
    def test_depositar_valor_zero(self, conta):
        """Testa depósito com valor zero."""
        resultado = conta.depositar(0)
        assert resultado is False
        assert conta.saldo == 0.0
    
    def test_sacar_valor_positivo_com_saldo(self, conta):
        """Testa saque com saldo suficiente."""
        conta.depositar(200.0)
        resultado = conta.sacar(100.0)
        assert resultado is True
        assert conta.saldo == 100.0
    
    def test_sacar_valor_maior_que_saldo(self, conta):
        """Testa saque com valor maior que o saldo."""
        conta.depositar(50.0)
        resultado = conta.sacar(100.0)
        assert resultado is False
        assert conta.saldo == 50.0
    
    def test_sacar_valor_negativo(self, conta):
        """Testa saque com valor negativo."""
        resultado = conta.sacar(-50.0)
        assert resultado is False
        assert conta.saldo == 0.0
    
    def test_nova_conta_factory_method(self, cliente):
        """Testa o método de fábrica nova_conta."""
        conta = Conta.nova_conta(cliente, 2)
        assert conta.numero == 2
        assert conta in cliente.contas


class TestContaCorrente:
    """Testes para a classe ContaCorrente."""
    
    def test_criar_conta_corrente(self, conta_corrente):
        """Testa a criação de uma conta corrente."""
        assert conta_corrente.limite == 1000.0
        assert conta_corrente.limite_saques == 3
    
    def test_saque_dentro_limite_valor(self, conta_corrente):
        """Testa saque dentro do limite de valor."""
        conta_corrente.depositar(500.0)
        resultado = conta_corrente.sacar(400.0)
        assert resultado is True
        assert conta_corrente.saldo == 100.0
    
    def test_saque_acima_limite_valor(self, conta_corrente):
        """Testa saque acima do limite de valor."""
        conta_corrente.depositar(2000.0)
        resultado = conta_corrente.sacar(1500.0)
        assert resultado is False
        assert conta_corrente.saldo == 2000.0
    
    def test_limite_saques_diarios(self, conta_corrente):
        """Testa o limite de saques diários."""
        conta_corrente.depositar(1000.0)
        
        # Realiza 3 saques (limite)
        assert conta_corrente.sacar(100.0) is True
        assert conta_corrente.sacar(100.0) is True
        assert conta_corrente.sacar(100.0) is True
        
        # Quarto saque deve falhar
        assert conta_corrente.sacar(100.0) is False


class TestTransacoes:
    """Testes para as classes de transação."""
    
    def test_deposito_registrar(self, conta):
        """Testa o registro de um depósito."""
        deposito = Deposito(200.0)
        deposito.registrar(conta)
        
        assert conta.saldo == 200.0
        assert len(conta.historico.transacoes) == 1
        assert conta.historico.transacoes[0]['tipo'] == 'Deposito'
        assert conta.historico.transacoes[0]['valor'] == 200.0
    
    def test_saque_registrar(self, conta):
        """Testa o registro de um saque."""
        conta.depositar(300.0)
        saque = Saque(100.0)
        saque.registrar(conta)
        
        assert conta.saldo == 200.0
        assert len(conta.historico.transacoes) == 2  # Depósito + Saque
        assert conta.historico.transacoes[1]['tipo'] == 'Saque'
        assert conta.historico.transacoes[1]['valor'] == 100.0
    
    def test_saque_sem_saldo(self, conta):
        """Testa saque sem saldo suficiente."""
        saque = Saque(100.0)
        saque.registrar(conta)
        
        assert conta.saldo == 0.0
        assert len(conta.historico.transacoes) == 0  # Transação não registrada


class TestCliente:
    """Testes para a classe Cliente."""
    
    def test_criar_pessoa_fisica(self):
        """Testa a criação de uma pessoa física."""
        data_nasc = date(1985, 5, 15)
        cliente = PessoaFisica(
            cpf="98765432100",
            nome="Maria Silva",
            data_nascimento=data_nasc,
            endereco="Av. Central, 456"
        )
        
        assert cliente.cpf == "98765432100"
        assert cliente.nome == "Maria Silva"
        assert cliente.data_nascimento == data_nasc
        assert cliente.identificar() == "98765432100"
    
    def test_adicionar_conta_cliente(self, cliente, conta):
        """Testa adicionar conta a um cliente."""
        cliente.adicionar_conta(conta)
        assert len(cliente.contas) == 1
        assert conta in cliente.contas
    
    def test_realizar_transacao(self, cliente, conta):
        """Testa realizar transação através do cliente."""
        cliente.adicionar_conta(conta)
        
        deposito = Deposito(500.0)
        cliente.realizar_transacao(conta, deposito)
        
        assert conta.saldo == 500.0
        assert len(conta.historico.transacoes) == 1


class TestHistorico:
    """Testes para a classe Historico."""
    
    def test_adicionar_transacao_historico(self, conta):
        """Testa adicionar transação ao histórico."""
        deposito = Deposito(100.0)
        deposito.registrar(conta)
        
        historico = conta.historico
        assert len(historico.transacoes) == 1
        assert historico.transacoes[0]['valor'] == 100.0
        assert historico.transacoes[0]['tipo'] == 'Deposito'
    
    def test_gerar_extrato_vazio(self):
        """Testa gerar extrato de histórico vazio."""
        historico = Historico()
        assert historico.gerar_extrato() == "Não foram realizadas movimentações."
    
    def test_gerar_extrato_com_transacoes(self, conta):
        """Testa gerar extrato com transações."""
        Deposito(100.0).registrar(conta)
        Deposito(50.0).registrar(conta)
        Saque(30.0).registrar(conta)
        
        extrato = conta.historico.gerar_extrato()
        assert "Deposito: R$ 100.00" in extrato
        assert "Deposito: R$ 50.00" in extrato
        assert "Saque: R$ 30.00" in extrato


if __name__ == "__main__":
    pytest.main(["-v", "test_conta.py"])