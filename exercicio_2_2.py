import os
from datetime import datetime
from pathlib import Path

from pymongo import MongoClient


def converter_linha(linha):
    partes = linha.split()
    campos = {}

    for item in partes[3:]:
        chave, valor = item.split("=", 1)
        campos[chave] = valor

    return {
        "timestamp": datetime.fromisoformat(f"{partes[0]}T{partes[1]}"),
        "fonte": "auth",
        "tipo": partes[2],
        **campos,
    }


arquivo = Path(__file__).with_name("auth.log")
documentos = []

for linha in arquivo.read_text(encoding="utf-8").splitlines():
    if linha.strip():
        documentos.append(converter_linha(linha))

cliente = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
eventos = cliente["seguranca"]["eventos"]

if documentos:
    eventos.insert_many(documentos)

pipeline = [
    {"$match": {"tipo": "FAIL"}},
    {"$group": {"_id": "$ip", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}},
    {"$limit": 5},
]

print("=== Top IPs por falhas de login ===")
for resultado in eventos.aggregate(pipeline):
    print(f"{resultado['_id']} -> {resultado['total']} falhas")

print(f"Total de eventos inseridos: {len(documentos)}")
