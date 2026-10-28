import os

import mysql.connector
from flask import Flask, jsonify, request
from mysql.connector import Error, IntegrityError


app = Flask(__name__)


def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "senha"),
        database=os.getenv("MYSQL_DATABASE", "seguranca"),
    )


@app.route("/api/usuarios", methods=["GET", "POST"])
def rota_usuarios():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)

            if request.method == "GET":
                cursor.execute(
                    "SELECT id, nome, email, nivel_acesso FROM usuarios"
                )
                return jsonify(cursor.fetchall())

            dados = request.get_json(silent=True) or {}

            if not dados.get("nome") or not dados.get("email"):
                return jsonify(erro="Corpo inválido."), 400

            try:
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, email, nivel_acesso)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        dados["nome"],
                        dados["email"],
                        dados.get("nivel_acesso", 1),
                    ),
                )
                conexao.commit()
                return jsonify(id=cursor.lastrowid), 201
            except IntegrityError:
                return jsonify(erro="E-mail já cadastrado."), 409

    except Error:
        return jsonify(erro="Serviço indisponível."), 500


@app.route(
    "/api/usuarios/<int:usuario_id>",
    methods=["GET", "PUT", "DELETE"],
)
def rota_usuario(usuario_id):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)

            cursor.execute(
                "SELECT id FROM usuarios WHERE id = %s",
                (usuario_id,),
            )

            if cursor.fetchone() is None:
                return jsonify(erro="Usuário não encontrado."), 404

            if request.method == "GET":
                cursor.execute(
                    """
                    SELECT id, nome, email, nivel_acesso
                    FROM usuarios
                    WHERE id = %s
                    """,
                    (usuario_id,),
                )
                return jsonify(cursor.fetchone())

            if request.method == "DELETE":
                cursor.execute(
                    "DELETE FROM usuarios WHERE id = %s",
                    (usuario_id,),
                )
                conexao.commit()
                return jsonify(mensagem="Removido")

            dados = request.get_json(silent=True) or {}

            if not dados.get("nome") or not dados.get("email"):
                return jsonify(erro="Corpo inválido."), 400

            try:
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET nome = %s,
                        email = %s,
                        nivel_acesso = %s
                    WHERE id = %s
                    """,
                    (
                        dados["nome"],
                        dados["email"],
                        dados.get("nivel_acesso", 1),
                        usuario_id,
                    ),
                )
                conexao.commit()
                return jsonify(mensagem="Atualizado")
            except IntegrityError:
                return jsonify(erro="E-mail já cadastrado."), 409

    except Error:
        return jsonify(erro="Serviço indisponível."), 500


if __name__ == "__main__":
    app.run(debug=False)
