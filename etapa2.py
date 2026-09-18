clientes = []
contas = []
contador_conta = 1

while True:
    print("\nMenu Principal")
    print("1 - Cadastrar cliente")
    print("2 - Cadastrar conta")
    print("3 - Listar contas")
    print("4 - Procurar uma conta pelo número")
    print("5 - Consultar saldo")
    print("6 - Depositar")
    print("7 - Sacar")
    print("0 - Sair")
    
    opcao = input("Escolha a opção: ")
    
    if opcao == '1':
        # Exigência: cadastrar vários clientes
        nome = input("Nome do cliente: ")
        clientes.append(nome)
        print("Cliente cadastrado com sucesso!")
        
    elif opcao == '2':
        # Exigência: cadastrar várias contas (vinculando a um cliente que já existe)
        nome_cliente = input("Nome do cliente para vincular a conta: ")
        
        if nome_cliente in clientes:
            conta = {
                "numero": contador_conta,
                "cliente": nome_cliente,
                "saldo": 0.0
            }
            contas.append(conta)
            print(f"Conta número {contador_conta} criada para {nome_cliente}.")
            contador_conta += 1
        else:
            print("Cliente não encontrado. Cadastre o cliente primeiro na opção 1.")
            
    elif opcao == '3':
        # Exigência: listar contas
        for conta in contas:
            print(f"Conta: {conta['numero']} | Cliente: {conta['cliente']}")
            
    elif opcao == '4':
        # Exigência: procurar uma conta pelo número
        numero_busca = int(input("Número da conta: "))
        encontrou = False
        
        for conta in contas:
            if conta['numero'] == numero_busca:
                print(f"Conta {conta['numero']} | Cliente: {conta['cliente']} | Saldo: {conta['saldo']} R$")
                encontrou = True
                break
                
        if not encontrou:
            print("Conta não encontrada.")
            
    elif opcao == '5':
        # Exigência: consultar saldo
        numero_busca = int(input("Número da conta: "))
        encontrou = False
        
        for conta in contas:
            if conta['numero'] == numero_busca:
                print(f"Saldo da conta {conta['numero']}: {conta['saldo']} R$")
                encontrou = True
                break
                
        if not encontrou:
            print("Conta não encontrada.")
            
    elif opcao == '6':
        # Exigência: depositar
        numero_busca = int(input("Número da conta para depósito: "))
        for conta in contas:
            if conta['numero'] == numero_busca:
                deposito = float(input("Valor do depósito: "))
                if deposito > 0:
                    conta['saldo'] = conta['saldo'] + deposito
                    print("Depósito realizado.")
                else:
                    print("Valor inválido.")
                break
                
    elif opcao == '7':
        # Exigência: sacar
        numero_busca = int(input("Número da conta para saque: "))
        for conta in contas:
            if conta['numero'] == numero_busca:
                saque = float(input("Valor do saque: "))
                if saque > 0 and saque <= conta['saldo']:
                    conta['saldo'] = conta['saldo'] - saque
                    print("Saque realizado.")
                elif saque > conta['saldo']:
                    print("Cliente não possui saldo suficiente para o saque.")
                else:
                    print("Valor inválido.")
                break
                
    elif opcao == '0':
        print("Sessão finalizada.")
        break
        
    else:
        print("Opção inválida.")
