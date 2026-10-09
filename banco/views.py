from main import app
from flask import render_template, request, redirect, url_for, flash

clientes = []
contas = []
contador_conta = 1


# Menu principal
@app.route("/")
def menu():
    return render_template("menu.html")


# 1 - Cadastrar cliente
@app.route("/cliente", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()

        if nome:
            clientes.append(nome)
            flash(f"Cliente '{nome}' cadastrado com sucesso!")
        else:
            flash("Informe o nome do cliente.")

        return redirect(url_for("menu"))

    return render_template("cliente.html")


# 2 - Cadastrar conta
@app.route("/conta", methods=["GET", "POST"])
def cadastrar_conta():
    global contador_conta

    if request.method == "POST":
        nome_cliente = request.form.get(
            "nome_cliente", ""
        ).strip()

        if nome_cliente in clientes:
            conta = {
                "numero": contador_conta,
                "cliente": nome_cliente,
                "saldo": 0.0
            }

            contas.append(conta)

            flash(
                f"Conta {contador_conta} criada para "
                f"{nome_cliente}. Saldo inicial: R$ 0,00."
            )

            contador_conta += 1
        else:
            flash(
                "Cliente não encontrado. "
                "Cadastre o cliente primeiro."
            )

        return redirect(url_for("menu"))

    return render_template("conta.html")


# 3 - Listar contas
@app.route("/contas")
def listar_contas():
    if not contas:
        flash("Nenhuma conta cadastrada.")
    else:
        flash(f"Total de contas cadastradas: {len(contas)}.")

        for conta in contas:
            flash(
                f"Conta {conta['numero']} | "
                f"Cliente: {conta['cliente']} | "
                f"Saldo: R$ {conta['saldo']:.2f}"
            )

    return redirect(url_for("menu"))


# 4 - Procurar conta pelo número
@app.route("/buscar-conta", methods=["GET", "POST"])
def buscar_conta():
    if request.method == "POST":
        numero = request.form.get("numero", "").strip()

        try:
            numero = int(numero)
            conta = localizar_conta(numero)

            if conta:
                flash(
                    f"Conta {conta['numero']} | "
                    f"Cliente: {conta['cliente']} | "
                    f"Saldo: R$ {conta['saldo']:.2f}"
                )
            else:
                flash("Conta não encontrada.")

        except ValueError:
            flash("Informe um número de conta válido.")

        return redirect(url_for("menu"))

    return render_template("buscar_conta.html")


# Função auxiliar para localizar uma conta
def localizar_conta(numero):
    for conta in contas:
        if conta["numero"] == numero:
            return conta

    return None


# 5 - Depositar
@app.route("/depositar", methods=["GET", "POST"])
def depositar():
    if request.method == "POST":
        try:
            numero = int(request.form.get("numero", ""))

            valor_texto = request.form.get("valor", "")
            valor = float(valor_texto.replace(",", "."))

            conta = localizar_conta(numero)

            if conta is None:
                flash("Conta não cadastrada.")
            elif valor <= 0:
                flash("O valor do depósito deve ser positivo.")
            else:
                conta["saldo"] += valor

                flash(
                    f"Depósito de R$ {valor:.2f} realizado "
                    f"na conta {numero}. "
                    f"Saldo atual: R$ {conta['saldo']:.2f}."
                )

        except ValueError:
            flash("Informe um número de conta e um valor válidos.")

        return redirect(url_for("menu"))

    return render_template(
        "operacao.html",
        titulo="Depositar",
        acao="depositar"
    )


# 6 - Sacar
@app.route("/sacar", methods=["GET", "POST"])
def sacar():
    if request.method == "POST":
        try:
            numero = int(request.form.get("numero", ""))

            valor_texto = request.form.get("valor", "")
            valor = float(valor_texto.replace(",", "."))

            conta = localizar_conta(numero)

            if conta is None:
                flash("Conta não cadastrada.")
            elif valor <= 0:
                flash("O valor do saque deve ser positivo.")
            elif valor > conta["saldo"]:
                flash("Saldo insuficiente para realizar o saque.")
            else:
                conta["saldo"] -= valor

                flash(
                    f"Saque de R$ {valor:.2f} realizado "
                    f"na conta {numero}. "
                    f"Saldo atual: R$ {conta['saldo']:.2f}."
                )

        except ValueError:
            flash("Informe um número de conta e um valor válidos.")

        return redirect(url_for("menu"))

    return render_template(
        "operacao.html",
        titulo="Sacar",
        acao="sacar"
    )