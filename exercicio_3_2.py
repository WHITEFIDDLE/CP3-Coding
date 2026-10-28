import os

import mysql.connector


configuracao = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "senha"),
    "database": os.getenv("MYSQL_DATABASE", "seguranca"),
}


def buscar_inseguro(nome):
    with mysql.connector.connect(**configuracao) as conexao:
        cursor = conexao.cursor()
        consulta = f"SELECT * FROM usuarios WHERE nome = '{nome}'"
        cursor.execute(consulta)
        return cursor.fetchall()


def buscar_seguro(nome):
    with mysql.connector.connect(**configuracao) as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
        return cursor.fetchall()


entrada = "' OR '1'='1"
resultado_inseguro = buscar_inseguro(entrada)
resultado_seguro = buscar_seguro(entrada)

print(f"[INSEGURO] {len(resultado_inseguro)} usuários retornados")
print(f"[SEGURO] {len(resultado_seguro)} usuários retornados")
print("A consulta parametrizada tratou a entrada como texto comum.")
