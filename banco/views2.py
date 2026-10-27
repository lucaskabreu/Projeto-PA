from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash_messages"

# --- CLASSES DO SEU SISTEMA ---

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
        self._saldo = 0.0  # Usando um underline para facilitar o acesso controlado por property

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True, "Depósito realizado com sucesso."
        return False, "Valor de depósito inválido."

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True, "Saque realizado com sucesso."
        elif valor > self._saldo:
            return False, "Cliente não possui saldo suficiente para o saque."
        else:
            return False, "Valor de saque inválido."

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

# --- INICIALIZAÇÃO DOS OBJETOS GLOBAIS ---
meuBanco = Banco("BB")
contador_conta = 1


# --- ROTAS DO FLASK ---

@app.route("/")
def menu():
    return render_template("menu.html", banco_nome=meuBanco.nome)


@app.route("/cliente", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        email = request.form.get("email", "").strip()
        idade_texto = request.form.get("idade", "").strip()

        if nome and cpf and email and idades_texto:
            try:
                idade = int(idade_texto)
                novo_cliente = Cliente(nome, cpf, email, idade)
                meuBanco.adicionar_cliente(novo_cliente)
                flash(f"Cliente '{nome}' cadastrado com sucesso no banco {meuBanco.nome}!")
                return redirect(url_for("menu"))
            except ValueError:
                flash("A idade deve ser um número inteiro válido.")
        else:
            flash("Todos os campos do cliente são obrigatórios.")

    return render_template("cliente.html")


@app.route("/conta", methods=["GET", "POST"])
def cadastrar_conta():
    global contador_conta

    if request.method == "POST":
        nome_cliente = request.form.get("nome_cliente", "").strip()
        cliente = meuBanco.procurar_cliente(nome_cliente)

        if cliente:
            nova_conta = Conta(contador_conta, cliente)
            meuBanco.adicionar_conta(nova_conta)
            flash(f"Conta número {contador_conta} criada com sucesso para o cliente {nome_cliente}!")
            contador_conta += 1
            return redirect(url_for("menu"))
        else:
            flash("Cliente não encontrado. Cadastre o cliente primeiro.")

    return render_template("conta.html")


@app.route("/contas")
def listar_contas():
    # Passamos a lista diretamente para o HTML renderizar a tabela dinamicamente
    return render_template("listar_contas.html", contas=meuBanco.contas)


@app.route("/buscar-conta", methods=["GET", "POST"])
def buscar_conta():
    if request.method == "POST":
        numero_texto = request.form.get("numero", "").strip()

        try:
            numero = int(numero_texto)
            conta = meuBanco.procurar_conta(numero)

            if conta:
                flash(f"Conta {conta.numero} | Cliente: {conta.cliente.nome} | CPF: {conta.cliente.cpf} | Saldo: R$ {conta.saldo:.2f}")
            else:
                flash("Conta não encontrada.")
        except ValueError:
            flash("Informe um número de conta válido.")

        return redirect(url_for("menu"))

    return render_template("buscar_conta.html")


@app.route("/depositar", methods=["GET", "POST"])
def depositar():
    if request.method == "POST":
        try:
            numero = int(request.form.get("numero", ""))
            valor = float(request.form.get("valor", "").replace(",", "."))

            conta = meuBanco.procurar_conta(numero)

            if conta:
                sucesso, mensagem = conta.depositar(valor)
                if sucesso:
                    flash(f"{mensagem} Saldo atual da conta {numero}: R$ {conta.saldo:.2f}")
                else:
                    flash(mensagem)
            else:
                flash("Conta não encontrada.")
        except ValueError:
            flash("Informe valores válidos para a conta e para o depósito.")

        return redirect(url_for("menu"))

    return render_template("operacao.html", titulo="Depositar", acao="depositar")


@app.route("/sacar", methods=["GET", "POST"])
def sacar():
    if request.method == "POST":
        try:
            numero = int(request.form.get("numero", ""))
            valor = float(request.form.get("valor", "").replace(",", "."))

            conta = meuBanco.procurar_conta(numero)

            if conta:
                sucesso, mensagem = conta.sacar(valor)
                if sucesso:
                    flash(f"{mensagem} Saldo atual da conta {numero}: R$ {conta.saldo:.2f}")
                else:
                    flash(mensagem)
            else:
                flash("Conta não encontrada.")
        except ValueError:
            flash("Informe valores válidos para a conta e para o saque.")

        return redirect(url_for("menu"))

    return render_template("operacao.html", titulo="Sacar", acao="sacar")


if __name__ == "__main__":
    app.run(debug=True)
