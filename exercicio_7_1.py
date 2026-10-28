import os
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

cliente = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
incidentes = cliente["seguranca"]["incidentes"]


def transformar_documento(documento):
    documento["id"] = str(documento.pop("_id"))
    documento["criado_em"] = documento["criado_em"].isoformat()
    return documento


def converter_id(texto):
    try:
        return ObjectId(texto)
    except InvalidId:
        return None


@app.route("/api/incidentes", methods=["GET", "POST"])
def rota_incidentes():
    if request.method == "GET":
        documentos = incidentes.find().sort("criado_em", -1)
        return jsonify([transformar_documento(doc) for doc in documentos])

    dados = request.get_json(silent=True) or {}
    obrigatorios = ("titulo", "severidade", "ip_origem")

    if not all(dados.get(campo) for campo in obrigatorios):
        return jsonify(erro="Campos obrigatórios ausentes."), 400

    dados["status"] = dados.get("status", "aberto")
    dados["criado_em"] = datetime.now(timezone.utc)

    resultado = incidentes.insert_one(dados)
    return jsonify(id=str(resultado.inserted_id)), 201


@app.route("/api/incidentes/<incidente_id>", methods=["GET", "PUT", "DELETE"])
def rota_incidente(incidente_id):
    object_id = converter_id(incidente_id)

    if object_id is None:
        return jsonify(erro="ID inválido."), 400

    if request.method == "GET":
        documento = incidentes.find_one({"_id": object_id})

        if documento is None:
            return jsonify(erro="Incidente não encontrado."), 404

        return jsonify(transformar_documento(documento))

    if request.method == "DELETE":
        resultado = incidentes.delete_one({"_id": object_id})

        if resultado.deleted_count == 0:
            return jsonify(erro="Incidente não encontrado."), 404

        return jsonify(mensagem="Removido")

    dados = request.get_json(silent=True) or {}
    campos_permitidos = ("titulo", "severidade", "status", "ip_origem")
    alteracoes = {}

    for campo in campos_permitidos:
        if campo in dados:
            alteracoes[campo] = dados[campo]

    resultado = incidentes.update_one(
        {"_id": object_id},
        {"$set": alteracoes},
    )

    if resultado.matched_count == 0:
        return jsonify(erro="Incidente não encontrado."), 404

    return jsonify(mensagem="Atualizado")


if __name__ == "__main__":
    app.run(debug=False)
