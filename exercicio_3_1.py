import os

import mysql.connector
from mysql.connector import IntegrityError


def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "senha"),
        database=os.getenv("MYSQL_DATABASE", "seguranca"),
    )


def cadastrar():
    nome = input("Nome: ")
    email = input("E-mail: ")
    nivel = int(input("Nível de acesso (1 a 5): "))

    if nivel < 1 or nivel > 5:
        print("Nível inválido.")
        return

    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, nivel_acesso)
                VALUES (%s, %s, %s)
                """,
                (nome, email, nivel),
            )
            conexao.commit()

        print("Usuário cadastrado!")

    except IntegrityError:
        print("Erro: e-mail já existe.")


def listar():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT nome, email, nivel_acesso
            FROM usuarios
            """
        )

        for nome, email, nivel in cursor.fetchall():
            print(f"{nome} | {email} | nível {nivel}")


def buscar():
    email = input("E-mail: ")

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT nome, email, nivel_acesso
            FROM usuarios
            WHERE email = %s
            """,
            (email,),
        )
        usuario = cursor.fetchone()

    print(usuario or "Usuário não encontrado.")


def alterar_nivel():
    email = input("E-mail: ")
    nivel = int(input("Novo nível (1 a 5): "))

    if nivel < 1 or nivel > 5:
        print("Nível inválido.")
        return

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            UPDATE usuarios
            SET nivel_acesso = %s
            WHERE email = %s
            """,
            (nivel, email),
        )
        conexao.commit()
        alterou = cursor.rowcount > 0

    if alterou:
        print("Nível atualizado!")
    else:
        print("Usuário não encontrado.")


def remover():
    email = input("E-mail: ")

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "DELETE FROM usuarios WHERE email = %s",
            (email,),
        )
        conexao.commit()
        removeu = cursor.rowcount > 0

    if removeu:
        print("Usuário removido!")
    else:
        print("Usuário não encontrado.")


opcoes = {
    "1": cadastrar,
    "2": listar,
    "3": buscar,
    "4": alterar_nivel,
    "5": remover,
}

while True:
    print()
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Buscar")
    print("4 - Alterar nível")
    print("5 - Remover")
    print("6 - Sair")

    opcao = input("Escolha: ")

    if opcao == "6":
        break

    acao = opcoes.get(opcao)

    if acao:
        acao()
    else:
        print("Opção inválida.")
