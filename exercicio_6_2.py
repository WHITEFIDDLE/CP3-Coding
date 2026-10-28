import re

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.post("/api/analisar-senha")
def analisar_senha():
    dados = request.get_json(silent=True) or {}
    senha = dados.get("senha")

    if not isinstance(senha, str):
        return jsonify(erro="Campo 'senha' obrigatório."), 400

    criterios = {
        "tamanho_min": len(senha) >= 8,
        "maiuscula": bool(re.search(r"[A-Z]", senha)),
        "minuscula": bool(re.search(r"[a-z]", senha)),
        "numero": bool(re.search(r"\d", senha)),
        "especial": bool(re.search(r"[^A-Za-z0-9]", senha)),
    }

    pontos = sum(criterios.values())

    if pontos == 5:
        forca = "Muito forte"
    elif pontos >= 4:
        forca = "Forte"
    elif pontos >= 3:
        forca = "Média"
    else:
        forca = "Fraca"

    return jsonify(forca=forca, criterios=criterios)


if __name__ == "__main__":
    app.run(debug=False)
