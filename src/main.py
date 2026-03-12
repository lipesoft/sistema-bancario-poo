import os
from datetime import date, datetime
from typing import List, Optional

from src.cliente import PessoaFisica
from src.conta import Conta, ContaCorrente
from src.transacao import Deposito, Saque


def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def encontrar_cliente_por_cpf(clientes: List[PessoaFisica], cpf: str) -> Optional[PessoaFisica]:
    """
    Busca um cliente pelo CPF.
    
    Args:
        clientes: Lista de clientes
        cpf: CPF a ser buscado
    
    Returns:
        Cliente encontrado ou None
    """
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def menu() -> str:
    """Exibe o menu principal e retorna a opção escolhida."""
    print("\n" + "=" * 50)
    print(" " * 15 + "🏦 SISTEMA BANCÁRIO 🏦")
    print("=" * 50)
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[nc] Nova conta")
    print("[lc] Listar contas")
    print("[nu] Novo cliente")
    print("[q] Sair")
    print("=" * 50)
    return input("=> ").strip().lower()


def depositar(clientes: List[PessoaFisica]):
    """Função para realizar um depósito."""
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = encontrar_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print("❌ Cliente não encontrado!")
        return
    
    if not cliente.contas:
        print("❌ Cliente não possui conta!")
        return
    
    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        transacao = Deposito(valor)
        
        # Considerando a primeira conta do cliente (simplificação)
        conta = cliente.contas[0]
        cliente.realizar_transacao(conta, transacao)
        
    except ValueError:
        print("❌ Valor inválido!")


def sacar(clientes: List[PessoaFisica]):
    """Função para realizar um saque."""
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = encontrar_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print("❌ Cliente não encontrado!")
        return
    
    if not cliente.contas:
        print("❌ Cliente não possui conta!")
        return
    
    try:
        valor = float(input("Informe o valor do saque: R$ "))
        transacao = Saque(valor)
        
        # Considerando a primeira conta do cliente (simplificação)
        conta = cliente.contas[0]
        cliente.realizar_transacao(conta, transacao)
        
    except ValueError:
        print("❌ Valor inválido!")


def exibir_extrato(clientes: List[PessoaFisica]):
    """Função para exibir o extrato da conta."""
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = encontrar_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print("❌ Cliente não encontrado!")
        return
    
    if not cliente.contas:
        print("❌ Cliente não possui conta!")
        return
    
    conta = cliente.contas[0]  # Considerando a primeira conta
    
    print("\n" + "=" * 50)
    print(" " * 16 + "📊 EXTRATO 📊")
    print("=" * 50)
    print(f"Cliente: {cliente.nome}")
    print(f"CPF: {cliente.cpf}")
    print(f"Agência: {conta.agencia} | Conta: {conta.numero}")
    print("-" * 50)
    
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    
    print("-" * 50)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("=" * 50)


def criar_cliente(clientes: List[PessoaFisica]):
    """Função para criar um novo cliente."""
    print("\n" + "=" * 50)
    print(" " * 16 + "👤 NOVO CLIENTE 👤")
    print("=" * 50)
    
    cpf = input("Informe o CPF (somente números): ")
    cliente_existente = encontrar_cliente_por_cpf(clientes, cpf)
    
    if cliente_existente:
        print("❌ Já existe cliente com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    
    try:
        data_str = input("Informe a data de nascimento (dd/mm/aaaa): ")
        dia, mes, ano = map(int, data_str.split('/'))
        data_nascimento = date(ano, mes, dia)
        
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")
        
        cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
        clientes.append(cliente)
        
        print("✅ Cliente criado com sucesso!")
        
    except ValueError:
        print("❌ Data inválida! Use o formato dd/mm/aaaa.")


def criar_conta(numero_conta: int, clientes: List[PessoaFisica], contas: List[Conta]):
    """Função para criar uma nova conta corrente."""
    print("\n" + "=" * 50)
    print(" " * 16 + "💰 NOVA CONTA 💰")
    print("=" * 50)
    
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = encontrar_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print("❌ Cliente não encontrado! Crie um cliente primeiro.")
        return None
    
    # Opção de configurar limites personalizados
    usar_padrao = input("Usar limites padrão (R$500,00 e 3 saques/dia)? (s/n): ").lower()
    
    if usar_padrao == 's':
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
    else:
        try:
            limite = float(input("Informe o limite por saque: R$ "))
            limite_saques = int(input("Informe o limite diário de saques: "))
            conta = ContaCorrente(cliente=cliente, numero=numero_conta, 
                                   limite=limite, limite_saques=limite_saques)
            cliente.adicionar_conta(conta)
        except ValueError:
            print("❌ Valores inválidos! Usando limites padrão.")
            conta = ContaCorrente.nova_conta(cliente, numero_conta)
    
    contas.append(conta)
    print(f"✅ Conta {numero_conta} criada com sucesso para {cliente.nome}!")
    return conta


def listar_contas(contas: List[Conta]):
    """Função para listar todas as contas cadastradas."""
    print("\n" + "=" * 50)
    print(" " * 16 + "📋 CONTAS CADASTRADAS 📋")
    print("=" * 50)
    
    if not contas:
        print("Não há contas cadastradas.")
        return
    
    for i, conta in enumerate(contas, 1):
        print(f"\n{i}. {conta}")
        print(f"   Titular: {conta.cliente.nome}")
        print(f"   Histórico: {len(conta.historico)} transação(ões)")
    
    print("\n" + "=" * 50)


def main():
    """Função principal do sistema."""
    clientes: List[PessoaFisica] = []
    contas: List[Conta] = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)
        
        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "nu":
            criar_cliente(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q":
            print("\n" + "=" * 50)
            print(" " * 16 + "👋 ATÉ LOGO! 👋")
            print("=" * 50)
            break
        
        else:
            print("❌ Operação inválida! Selecione novamente.")
        
        input("\nPressione Enter para continuar...")
        limpar_tela()


if __name__ == "__main__":
    main()