---- Cadastro de um cliente
print("Nome do cliente: ")
clienteNome = input()

clienteConta = "0001"
print(f"O número da conta do cliente é {clienteConta}")

clenteSaldo = 0

print("Valor do depósito: ")
deposito = float(input())
clienteSaldo = clienteSaldo + deposito

print("Valor do saque: ")
saque = float(input())
if saque <= clienteSaldo:
  clienteSaldo = cliente - saque
else:
  print("Cliente não possui saldo suficiente para o saldo")

print(f"O atual saldo do cliente é de {saldoCliente} R$")

