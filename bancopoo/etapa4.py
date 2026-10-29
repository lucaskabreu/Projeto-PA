class Cliente:
    def __init__(self, nome, cpf, email, idade):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.idade = idade

class Conta:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.__saldo = 0.0
    
    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print("Depósito realizado.")
        else:
            print("Valor inválido.")

    def sacar(self, valor):
        if valor <= self.__saldo and valor > 0:
            self.__saldo -= valor
            print("Saque realizado.")
        elif valor > self.__saldo:
            print("Cliente não possui saldo suficiente para o saque.")
        else:
            print("Valor inválido.")

    def exibir_saldo(self):
        print(f"Conta {self.numero} | Cliente: {self.cliente.nome} | Saldo: {self.__saldo:.2f} R$")

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.contas = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def procurar_cliente(self, nome):
        for cliente in self.clientes:
            if cliente.nome == nome:
                return cliente
        return None

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def listar_contas(self):
        for conta in self.contas:
            print(f"Conta: {conta.numero} | Cliente: {conta.cliente.nome} | Saldo: {conta._Conta__saldo:.2f} R$")

    def procurar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

contador_conta = 1
meuBanco = Banco("BB")

while True:
    print("\nMenu Principal")
    print("1 - Cadastrar cliente")
    print("2 - Cadastrar conta")
    print("3 - Listar contas")
    print("4 - Procurar uma conta pelo número")
    print("5 - Depositar")
    print("6 - Sacar")
    print("0 - Sair")

    opcao = int(input("Escolha a opção: "))

    if opcao == 1:
        nome_cliente = input("Nome do cliente: ")
        cpf_cliente = input("CPF do cliente: ")
        email_cliente = input("Email do cliente: ")
        idade_cliente = int(input("Idade do cliente: "))
        cliente = Cliente(nome_cliente, cpf_cliente, email_cliente, idade_cliente)
        print(f"Cliente {nome_cliente} cadastrado com sucesso.")
        meuBanco.adicionar_cliente(cliente)

    elif opcao == 2:
        nome_cliente = input("Nome do cliente para vincular a conta: ")
        cliente = meuBanco.procurar_cliente(nome_cliente)

        if cliente:
            conta = Conta(contador_conta, cliente)
            meuBanco.adicionar_conta(conta)
            print(f"Conta número {contador_conta} criada para {nome_cliente}.")
            contador_conta += 1
        else:
            print("Cliente não encontrado. Cadastre o cliente primeiro na opção 1.")

    elif opcao == 3:
        meuBanco.listar_contas()

    elif opcao == 4:
        numero_busca = int(input("Número da conta: "))
        conta = meuBanco.procurar_conta(numero_busca)

        if conta:
            conta.exibir_saldo()
        else:
            print("Conta não encontrada.")

    elif opcao == 5:
        numero_busca = int(input("Número da conta para depósito: "))
        conta = meuBanco.procurar_conta(numero_busca)

        if conta:
            valor_deposito = float(input("Valor do depósito: "))
            conta.depositar(valor_deposito)
        else:
            print("Conta não encontrada.")

    elif opcao == 6:
        numero_busca = int(input("Número da conta para saque: "))
        conta = meuBanco.procurar_conta(numero_busca)

        if conta:
            valor_saque = float(input("Valor do saque: "))
            conta.sacar(valor_saque)
        else:
            print("Conta não encontrada.")

    elif opcao == 0:
        print("Sessão finalizada")
        break

    else:
        print("Opção inválida. Tente novamente.")
