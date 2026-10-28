import os
from datetime import datetime

from pymongo import MongoClient


cliente = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
eventos = cliente["seguranca"]["eventos"]


def consultar(fonte=None, tipo=None, ip=None, desde=None):
    filtro = {}

    if fonte is not None:
        filtro["fonte"] = fonte
    if tipo is not None:
        filtro["tipo"] = tipo
    if ip is not None:
        filtro["ip"] = ip
    if desde is not None:
        filtro["timestamp"] = {"$gte": desde}

    return list(eventos.find(filtro, {"_id": 0}).sort("timestamp", -1))


print(consultar(tipo="FAIL", ip="185.220.101.1"))
print(consultar(fonte="auth", desde=datetime(2025, 2, 20)))
