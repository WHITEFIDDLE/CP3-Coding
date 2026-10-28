from flask import Flask, jsonify, request


app = Flask(__name__)
usuarios = []
proximo_id = 1


def encontrar_usuario(usuario_id):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    return None


@app.route("/api/usuarios", methods=["GET", "POST"])
def rota_usuarios():
    global proximo_id

    if request.method == "GET":
        return jsonify(usuarios)

    dados = request.get_json(silent=True) or {}

    if not all(campo in dados for campo in ("nome", "email", "nivel")):
        return jsonify(erro="Campos obrigatórios ausentes."), 400

    if dados["nivel"] not in range(1, 6):
        return jsonify(erro="Nível inválido."), 400

    for usuario in usuarios:
        if usuario["email"] == dados["email"]:
            return jsonify(erro="E-mail já existe."), 400

    usuario = {
        "id": proximo_id,
        "nome": dados["nome"],
        "email": dados["email"],
        "nivel": dados["nivel"],
    }

    usuarios.append(usuario)
    proximo_id += 1
    return jsonify(usuario), 201


@app.route("/api/usuarios/<int:usuario_id>", methods=["GET", "PUT", "DELETE"])
def rota_usuario(usuario_id):
    usuario = encontrar_usuario(usuario_id)

    if usuario is None:
        return jsonify(erro="Usuário não encontrado."), 404

    if request.method == "GET":
        return jsonify(usuario)

    if request.method == "DELETE":
        usuarios.remove(usuario)
        return jsonify(mensagem="Removido")

    dados = request.get_json(silent=True) or {}

    if "nivel" in dados and dados["nivel"] not in range(1, 6):
        return jsonify(erro="Nível inválido."), 400

    usuario.update(dados)
    return jsonify(usuario)


if __name__ == "__main__":
    app.run(debug=False)
