
from flask import render_template, request, redirect, url_for, flash
from main import app

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

    def get_saldo(self):
        return self.__saldo

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return f"Depósito de R$ {valor:.2f} realizado com sucesso!"
        return "Valor inválido para depósito."

    def sacar(self, valor):
        if valor <= 0:
            return "Valor inválido para saque."
        elif valor > self.__saldo:
            return "Cliente não possui saldo suficiente para o saque."
        else:
            self.__saldo -= valor
            return f"Saque de R$ {valor:.2f} realizado com sucesso!"

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

    def procurar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None


contador_conta = 1
meuBanco = Banco("BB")

@app.route("/")
def menu():
    return render_template("menu.html")


# 1 - Cadastrar cliente
@app.route("/cliente", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        email = request.form.get("email", "").strip()
        idade_texto = request.form.get("idade", "").strip()

        try:
            idade = int(idade_texto)
            if nome and cpf and email:
                novo_cliente = Cliente(nome, cpf, email, idade)
                meuBanco.adicionar_cliente(novo_cliente)
                flash(f"Cliente '{nome}' cadastrado com sucesso!")
            else:
                flash("Preencha todos os campos do cliente.")
        except ValueError:
            flash("Informe uma idade válida.")

        return redirect(url_for("menu"))

    return render_template("cliente.html")


# 2 - Cadastrar conta
@app.route("/conta", methods=["GET", "POST"])
def cadastrar_conta():
    global contador_conta

    if request.method == "POST":
        nome_cliente = request.form.get("nome_cliente", "").strip()
        cliente = meuBanco.procurar_cliente(nome_cliente)

        if cliente:
            nova_conta = Conta(contador_conta, cliente)
            meuBanco.adicionar_conta(nova_conta)
            flash(f"Conta {contador_conta} criada para {nome_cliente}.")
            contador_conta += 1
        else:
            flash("Cliente não encontrado. Cadastre o cliente primeiro.")

        return redirect(url_for("menu"))

    return render_template("conta.html")


# 3 - Listar contas
@app.route("/contas")
def listar_contas():
    if not meuBanco.contas:
        flash("Nenhuma conta cadastrada.")
    else:
        flash(f"Total de contas cadastradas: {len(meuBanco.contas)}.")
        for conta in meuBanco.contas:
            flash(
                f"Conta {conta.numero} | "
                f"Cliente: {conta.cliente.nome} | "
                f"Saldo: R$ {conta.get_saldo():.2f}"
            )

    return redirect(url_for("menu"))


# 4 - Procurar conta pelo número
@app.route("/buscar-conta", methods=["GET", "POST"])
def buscar_conta():
    if request.method == "POST":
        numero_texto = request.form.get("numero", "").strip()

        try:
            numero = int(numero_texto)
            conta = meuBanco.procurar_conta(numero)

            if conta:
                flash(
                    f"Conta {conta.numero} | "
                    f"Cliente: {conta.cliente.nome} | "
                    f"Saldo: R$ {conta.get_saldo():.2f}"
                )
            else:
                flash("Conta não encontrada.")
        except ValueError:
            flash("Informe um número de conta válido.")

        return redirect(url_for("menu"))

    return render_template("buscar_conta.html")


# 5 e 6 - Depositar e Sacar
@app.route("/operacao/<tipo>", methods=["GET", "POST"])
def realizar_operacao(tipo):
    if request.method == "POST":
        try:
            numero = int(request.form.get("numero", ""))
            valor = float(request.form.get("valor", "").replace(",", "."))
            
            conta = meuBanco.procurar_conta(numero)

            if conta is None:
                flash("Conta não cadastrada.")
            else:
                if tipo == "depositar":
                    mensagem = conta.depositar(valor)
                elif tipo == "sacar":
                    mensagem = conta.sacar(valor)
                
                flash(f"{mensagem} Saldo atual: R$ {conta.get_saldo():.2f}")

        except ValueError:
            flash("Informe um número de conta e um valor válidos.")

        return redirect(url_for("menu"))

    titulo = "Depositar" if tipo == "depositar" else "Sacar"
    return render_template("operacao.html", titulo=titulo, acao=tipo)
