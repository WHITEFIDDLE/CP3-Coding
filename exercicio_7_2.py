import os

from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

cliente = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
incidentes = cliente["seguranca"]["incidentes"]


@app.get("/api/incidentes")
def listar_incidentes():
    try:
        pagina = int(request.args.get("pagina", 1))
        tamanho = int(request.args.get("tamanho", 10))
    except ValueError:
        return jsonify(erro="Paginação inválida."), 400

    pagina = max(pagina, 1)
    tamanho = min(max(tamanho, 1), 100)

    filtro = {}

    if request.args.get("severidade"):
        filtro["severidade"] = request.args["severidade"]

    if request.args.get("status"):
        filtro["status"] = request.args["status"]

    documentos = (
        incidentes.find(filtro)
        .sort("criado_em", -1)
        .skip((pagina - 1) * tamanho)
        .limit(tamanho)
    )

    itens = []

    for documento in documentos:
        documento["id"] = str(documento.pop("_id"))
        documento["criado_em"] = documento["criado_em"].isoformat()
        itens.append(documento)

    return jsonify(
        pagina=pagina,
        tamanho=tamanho,
        total=incidentes.count_documents(filtro),
        itens=itens,
    )


if __name__ == "__main__":
    app.run(debug=False)
