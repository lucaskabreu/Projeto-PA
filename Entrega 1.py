---- Cadastro de um cliente
print("Nome do cliente: ")
clienteNome = input()

---- Criação da conta
clienteConta = "0001"
print(f"O número da conta de {clienteNome} é {clienteConta}")

---- Variável que contém o saldo do cliente
clenteSaldo = 0

---- Realização de depósito
print("Valor do depósito: ")
deposito = float(input())
clienteSaldo = clienteSaldo + deposito

---- Realização de salque
print("Valor do saque: ")
saque = float(input())
if saque <= clienteSaldo:
  clienteSaldo = cliente - saque
else:
  print("Cliente não possui saldo suficiente para o saque")

---- Exibição de saldo do cliente
print(f"O atual saldo do cliente é de {saldoCliente} R$")
