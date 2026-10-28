import os

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


cliente = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
ativos = cliente["seguranca"]["ativos"]
ativos.create_index("ip", unique=True)

dados_iniciais = [
    {"nome": "SRV-WEB01", "tipo": "servidor", "ip": "192.168.1.10", "status": "ativo"},
    {"nome": "PC-RH03", "tipo": "estacao", "ip": "192.168.1.45", "status": "ativo"},
    {"nome": "SW-CORE01", "tipo": "switch", "ip": "192.168.1.1", "status": "inativo"},
]

for ativo in dados_iniciais:
    ativos.update_one({"ip": ativo["ip"]}, {"$setOnInsert": ativo}, upsert=True)


def cadastrar():
    ativo = {
        "nome": input("Nome: "),
        "tipo": input("Tipo: "),
        "ip": input("IP: "),
        "status": input("Status: "),
    }

    try:
        ativos.insert_one(ativo)
        print("Ativo cadastrado!")
    except DuplicateKeyError:
        print("Erro: IP já cadastrado!")


def listar():
    for ativo in ativos.find({}, {"_id": 0}):
        print(ativo)


def buscar():
    ip = input("IP: ")
    ativo = ativos.find_one({"ip": ip}, {"_id": 0})
    print(ativo or "Ativo não encontrado.")


def atualizar():
    ip = input("IP: ")
    status = input("Novo status: ")
    resultado = ativos.update_one({"ip": ip}, {"$set": {"status": status}})
    print("Status atualizado!" if resultado.matched_count else "Ativo não encontrado.")


def remover():
    ip = input("IP: ")
    resultado = ativos.delete_one({"ip": ip})
    print("Ativo removido!" if resultado.deleted_count else "Ativo não encontrado.")


opcoes = {
    "1": cadastrar,
    "2": listar,
    "3": buscar,
    "4": atualizar,
    "5": remover,
}

while True:
    print("\n1-Cadastrar  2-Listar  3-Buscar  4-Atualizar  5-Remover  6-Sair")
    opcao = input("Escolha: ")

    if opcao == "6":
        break

    acao = opcoes.get(opcao)
    if acao:
        acao()
    else:
        print("Opção inválida.")
