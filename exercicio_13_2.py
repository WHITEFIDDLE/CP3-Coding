import os
from collections import Counter

from openai import OpenAI


logs = [
    "GET /index.html ip=192.168.1.10 status=200",
    "GET /../../etc/passwd ip=91.240.118.172 status=400",
    "POST /login ip=185.220.101.1 status=401 (5x seguidas)",
]


def classificar_por_regras(log):
    texto = log.lower()

    if "../" in texto or "etc/passwd" in texto:
        return "CRITICO"

    if "5x" in texto or ("login" in texto and "401" in texto):
        return "SUSPEITO"

    return "NORMAL"


def classificar_com_api(log):
    cliente = OpenAI()

    resposta = cliente.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Classifique o log somente como "
                    "NORMAL, SUSPEITO ou CRITICO."
                ),
            },
            {
                "role": "user",
                "content": log,
            },
        ],
    )

    return resposta.choices[0].message.content.strip().upper()


def classificar(log):
    if not os.getenv("OPENAI_API_KEY"):
        return classificar_por_regras(log)

    try:
        resultado = classificar_com_api(log)

        if resultado in {"NORMAL", "SUSPEITO", "CRITICO"}:
            return resultado
    except Exception:
        pass

    return classificar_por_regras(log)


resultados = []

for log in logs:
    categoria = classificar(log)
    resultados.append(categoria)
    print(f"[{categoria}] {log}")

contagem = Counter(resultados)

print("\n=== Resumo ===")
print(f"NORMAL: {contagem['NORMAL']}")
print(f"SUSPEITO: {contagem['SUSPEITO']}")
print(f"CRITICO: {contagem['CRITICO']}")
