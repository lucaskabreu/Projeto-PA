
from flask import Flask, request, jsonify
from math import isfinite

app = Flask(__name__)


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
        return self.__saldo

    def depositar(self, valor):
        if not isfinite(valor) or valor <= 0:
            return False, "Valor inválido."

        self.__saldo += valor
        return True, "Depósito realizado com sucesso."

    def sacar(self, valor):
        if not isfinite(valor) or valor <= 0:
            return False, "Valor inválido."

        if valor > self.__saldo:
            return False, "Saldo insuficiente."

        self.__saldo -= valor
        return True, "Saque realizado com sucesso."


class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.contas = []
        self.contador_conta = 1

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def procurar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def criar_conta(self, cliente):
        conta = Conta(self.contador_conta, cliente)
        self.contas.append(conta)
        self.contador_conta += 1
        return conta

    def procurar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None


meuBanco = Banco("BB")


@app.route("/")
def inicio():
    return jsonify({
        "mensagem": "API do banco funcionando!",
        "rotas": {
            "cadastrar_cliente": "POST /clientes",
            "listar_clientes": "GET /clientes",
            "criar_conta": "POST /contas",
            "listar_contas": "GET /contas",
            "consultar_conta": "GET /contas/<numero>",
            "depositar": "POST /contas/<numero>/depositar",
            "sacar": "POST /contas/<numero>/sacar"
        }
    })


@app.route("/clientes", methods=["POST"])
def cadastrar_cliente():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados em JSON."}), 400

    campos = ["nome", "cpf", "email", "idade"]

    if any(campo not in dados for campo in campos):
        return jsonify({
            "erro": "Informe nome, cpf, email e idade."
        }), 400

    try:
        nome = dados["nome"]
        cpf = dados["cpf"]
        email = dados["email"]
        idade = int(dados["idade"])

        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in [nome, cpf, email]
        ):
            raise ValueError

        if idade <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({"erro": "Dados do cliente inválidos."}), 400

    if meuBanco.procurar_cliente(cpf):
        return jsonify({"erro": "CPF já cadastrado."}), 409

    cliente = Cliente(nome.strip(), cpf.strip(), email.strip(), idade)
    meuBanco.adicionar_cliente(cliente)

    return jsonify({
        "mensagem": "Cliente cadastrado com sucesso.",
        "nome": cliente.nome,
        "cpf": cliente.cpf
    }), 201


@app.route("/clientes", methods=["GET"])
def listar_clientes():
    return jsonify([
        {
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "email": cliente.email,
            "idade": cliente.idade
        }
        for cliente in meuBanco.clientes
    ])


@app.route("/contas", methods=["POST"])
def cadastrar_conta():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or "cpf" not in dados:
        return jsonify({
            "erro": "Informe o CPF do cliente."
        }), 400

    cpf = dados["cpf"]

    if not isinstance(cpf, str):
        return jsonify({"erro": "CPF inválido."}), 400

    cliente = meuBanco.procurar_cliente(cpf.strip())

    if cliente is None:
        return jsonify({
            "erro": "Cliente não encontrado. Cadastre-o primeiro."
        }), 404

    conta = meuBanco.criar_conta(cliente)

    return jsonify({
        "mensagem": "Conta criada com sucesso.",
        "numero": conta.numero,
        "cliente": cliente.nome,
        "saldo": conta.saldo
    }), 201


@app.route("/contas", methods=["GET"])
def listar_contas():
    return jsonify([
        {
            "numero": conta.numero,
            "cliente": conta.cliente.nome,
            "saldo": conta.saldo
        }
        for conta in meuBanco.contas
    ])


@app.route("/contas/<int:numero>", methods=["GET"])
def consultar_conta(numero):
    conta = meuBanco.procurar_conta(numero)

    if conta is None:
        return jsonify({"erro": "Conta não encontrada."}), 404

    return jsonify({
        "numero": conta.numero,
        "cliente": conta.cliente.nome,
        "saldo": conta.saldo
    })


def movimentar_conta(numero, operacao):
    conta = meuBanco.procurar_conta(numero)

    if conta is None:
        return jsonify({"erro": "Conta não encontrada."}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or "valor" not in dados:
        return jsonify({"erro": "Informe o valor da operação."}), 400

    try:
        valor = float(dados["valor"])
    except (ValueError, TypeError):
        return jsonify({"erro": "Informe um valor numérico válido."}), 400

    if not isfinite(valor):
        return jsonify({"erro": "Valor inválido."}), 400

    if operacao == "depositar":
        sucesso, mensagem = conta.depositar(valor)
    else:
        sucesso, mensagem = conta.sacar(valor)

    if not sucesso:
        return jsonify({"erro": mensagem}), 400

    return jsonify({
        "mensagem": mensagem,
        "conta": conta.numero,
        "saldo": conta.saldo
    })


@app.route("/contas/<int:numero>/depositar", methods=["POST"])
def depositar(numero):
    return movimentar_conta(numero, "depositar")


@app.route("/contas/<int:numero>/sacar", methods=["POST"])
def sacar(numero):
    return movimentar_conta(numero, "sacar")


if __name__ == "__main__":
    app.run(debug=True)
