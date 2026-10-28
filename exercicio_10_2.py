import json
import os

import requests


sessao = requests.Session()
sessao.headers["User-Agent"] = "exercicio-coding-for-security"

token = os.getenv("GITHUB_TOKEN")
if token:
    sessao.headers["Authorization"] = f"Bearer {token}"


def consultar(caminho, parametros=None):
    url = f"https://api.github.com{caminho}"
    resposta = sessao.get(url, params=parametros, timeout=15)

    if resposta.status_code in (403, 429):
        raise RuntimeError("Limite de requisições atingido.")

    resposta.raise_for_status()
    return resposta.json()


usuario = input("Usuário do GitHub: ").strip()
perfil = None
repositorios = []

while True:
    print("\n1-Buscar usuário  2-Listar repositórios  3-Detalhar  4-Salvar  5-Sair")
    opcao = input("Escolha: ")

    try:
        if opcao == "1":
            perfil = consultar(f"/users/{usuario}")
            print(f"Nome: {perfil['name']}")
            print(f"Repositórios públicos: {perfil['public_repos']}")
            print(f"Seguidores: {perfil['followers']}")

        elif opcao == "2":
            repositorios = []
            pagina = 1

            while True:
                lote = consultar(
                    f"/users/{usuario}/repos",
                    {"page": pagina, "per_page": 100},
                )

                if not lote:
                    break

                repositorios.extend(lote)
                pagina += 1

            for numero, repositorio in enumerate(repositorios, start=1):
                print(
                    f"{numero}. {repositorio['name']} | "
                    f"{repositorio['language']} | "
                    f"{repositorio['stargazers_count']} estrelas"
                )

        elif opcao == "3":
            nome = input("Nome do repositório: ")
            detalhes = consultar(f"/repos/{usuario}/{nome}")
            print(json.dumps(detalhes, indent=2, ensure_ascii=False))

        elif opcao == "4":
            nome_arquivo = f"github_{usuario}.json"
            dados = {"perfil": perfil, "repositorios": repositorios}

            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=2, ensure_ascii=False)

            print(f"Resultados salvos em {nome_arquivo}")

        elif opcao == "5":
            break

        else:
            print("Opção inválida.")

    except (requests.RequestException, RuntimeError) as erro:
        print(f"Erro: {erro}")
