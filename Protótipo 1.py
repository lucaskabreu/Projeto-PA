### Variável para continuar ou não realizando cadastros
respostaCadastro = 's'
### Variável para gerar número da conta do cliente
clienteConta = 0

#### Cadastro de um cliente
while (respostaCadastro == 'sim') or (respostaCadastro == 's'):
  print("Deseja cadastrar um novo cliente?")
  respostaCadastro = input()
  print("-----------------------")
  
  if (respostaCadastro == 'sim') or (respostaCadastro == 's'):
    print("Nome do cliente: ")
    clienteNome = input()
    print("-----------------------")

    #### Criação da conta
    clienteConta = clienteConta + 1
    if clienteConta < 10000:
        print(f"O número da conta de {clienteNome} é {clienteConta:04d}\n")
    else:
        print(f"O número da conta de {clienteNome} é {clienteConta}\n")

    #### Variável que contém o saldo do cliente
    clienteSaldo = 0

    print("Deseja realizar alguma operação para essa conta?")
    respostaOperação = input()
    print("-----------------------")
    while (respostaOperação == 'sim') or (respostaOperação == 's'):

        print("Selecione a operação:\n ")
        print("1) Depósito\n2) Saque\n-----------------------")
        selecionaOperação = input()
        print("-----------------------")


        if (selecionaOperação == '1') or  (selecionaOperação == 'deposito'):
          #### Realização de depósito
          print("Valor do depósito: ")
          deposito = float(input())
          while deposito <= 0:
              print("-----------------------")
              print("Valor inválido. Escolha outro valor: ")
              deposito = float(input())
          print("-----------------------")
          clienteSaldo = clienteSaldo + deposito
          print (f"Operação finalizada.\nO atual saldo do cliente {clienteConta:04d} é de {clienteSaldo:.2f} R$.")

    
        elif (selecionaOperação == '2') or (selecionaOperação == 'saque'):
           #### Realização de salque
            print("Valor do saque: ")
            saque = float(input())
            while saque <= 0:
              print("-----------------------")
              print("Valor inválido. Escolha outro valor: ")
              saque = float(input())

            print("-----------------------")
            if saque <= clienteSaldo:
              clienteSaldo = clienteSaldo - saque
            else:
              print("Cliente não possui saldo suficiente para o saque.")
              print("-----------------------")
            print (f"Operação finalizada.\nO atual saldo do cliente {clienteConta:04d} é de {clienteSaldo:.2f} R$.")

        else: 
          print("Operação inválida!")

        print("-----------------------")
        print("Deseja realizar uma nova operação para essa conta?")
        respostaOperação = input()
        print("-----------------------")

print("Sessão finalizada.")
    
