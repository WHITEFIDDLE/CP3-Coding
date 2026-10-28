import requests


def buscar_cve(cve_id):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    try:
        resposta = requests.get(
            url,
            params={"cveId": cve_id},
            timeout=15,
        )
        resposta.raise_for_status()
    except requests.Timeout:
        print("A consulta demorou demais.")
        return
    except requests.RequestException as erro:
        print(f"Erro ao consultar a API: {erro}")
        return

    itens = resposta.json().get("vulnerabilities", [])

    if not itens:
        print("CVE não encontrada.")
        return

    cve = itens[0]["cve"]

    descricao = "Sem descrição."
    for item in cve["descriptions"]:
        if item["lang"] == "en":
            descricao = item["value"]
            break

    metricas = cve.get("metrics", {})
    grupos_cvss = []

    for nome, grupo in metricas.items():
        if nome.startswith("cvssMetric"):
            grupos_cvss = grupo
            break

    if grupos_cvss:
        cvss = grupos_cvss[0]["cvssData"]
        pontuacao = cvss["baseScore"]
        severidade = cvss["baseSeverity"]
    else:
        pontuacao = "N/A"
        severidade = "N/A"

    print(cve_id)
    print(f"CVSS: {pontuacao} ({severidade})")
    print(f"Descrição: {descricao}")


cve_id = input("Digite a CVE: ").strip().upper()
buscar_cve(cve_id)
