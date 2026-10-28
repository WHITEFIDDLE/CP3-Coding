import ipaddress
import time

import requests


ips = [
    "8.8.8.8",
    "1.1.1.1",
    "185.220.101.1",
    "192.168.1.10",
    "8.8.8.8",
]

cache = {}
consultas_http = 0
acertos_cache = 0
enderecos_internos = 0


def consultar_ip(ip):
    global consultas_http, acertos_cache, enderecos_internos

    endereco = ipaddress.ip_address(ip)

    if endereco.is_private:
        enderecos_internos += 1
        return "Rede interna (não consultado)"

    if ip in cache:
        acertos_cache += 1
        return f"[CACHE] {cache[ip]}"

    url = f"https://ipapi.co/{ip}/json/"

    for tentativa in range(4):
        resposta = requests.get(url, timeout=10)

        if resposta.status_code != 429:
            resposta.raise_for_status()
            break

        time.sleep(2**tentativa)
    else:
        raise RuntimeError("O limite de requisições continuou ativo.")

    consultas_http += 1
    dados = resposta.json()

    texto = (
        f"{dados.get('city', '?')} / "
        f"{dados.get('country_code', '?')} / "
        f"{dados.get('org', '?')} (EXTERNO)"
    )

    cache[ip] = texto
    return texto


for ip in ips:
    try:
        print(f"{ip:<16} -> {consultar_ip(ip)}")
    except (ValueError, requests.RequestException, RuntimeError) as erro:
        print(f"{ip:<16} -> erro: {erro}")

print("\n=== Resumo ===")
print(f"Consultas HTTP: {consultas_http}")
print(f"Cache hits: {acertos_cache}")
print(f"Internos: {enderecos_internos}")
