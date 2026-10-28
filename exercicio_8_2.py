import os
import time
from collections import defaultdict

import mysql.connector
from flask import Flask, jsonify, request


app = Flask(__name__)

tentativas = defaultdict(list)
limite = 5
janela_em_segundos = 60


def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "senha"),
        database=os.getenv("MYSQL_DATABASE", "seguranca"),
    )


@app.post("/login")
def login():
    dados = request.get_json(silent=True) or {}
    usuario = dados.get("usuario", "")
    senha = dados.get("senha", "")

    if not usuario or not senha:
        return jsonify(erro="Usuário e senha são obrigatórios."), 400

    ip = request.remote_addr
    agora = time.time()

    tentativas[ip] = [
        instante
        for instante in tentativas[ip]
        if agora - instante < janela_em_segundos
    ]

    if len(tentativas[ip]) >= limite:
        return jsonify(erro="Muitas tentativas. Aguarde um minuto."), 429

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id
            FROM usuarios_login
            WHERE usuario = %s
              AND senha_hash = SHA2(%s, 256)
            """,
            (usuario, senha),
        )
        encontrado = cursor.fetchone()

    if encontrado is None:
        tentativas[ip].append(agora)
        return jsonify(erro="Credenciais inválidas."), 401

    tentativas[ip].clear()
    return jsonify(mensagem="Login OK")


if __name__ == "__main__":
    app.run(debug=False)

