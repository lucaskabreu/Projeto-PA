from flask import Flask

app = Flask(__name__)

# Necessário para utilizar mensagens entre rotas
app.secret_key = "chave-temporaria-desenvolvimento"

from views import *

if __name__ == "__main__":
    app.run(debug=True)