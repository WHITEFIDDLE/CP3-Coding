import os

from openai import OpenAI


cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

historico = [
    {
        "role": "system",
        "content": (
            "Responda em português como um assistente "
            "educacional de cibersegurança."
        ),
    }
]

while True:
    pergunta = input("Você: ").strip()

    if pergunta == "/sair":
        print("Assistente: Até logo!")
        break

    historico.append(
        {
            "role": "user",
            "content": pergunta,
        }
    )

    try:
        resposta = cliente.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages=historico,
        )

        texto = resposta.choices[0].message.content

        historico.append(
            {
                "role": "assistant",
                "content": texto,
            }
        )

        print(f"Assistente: {texto}")

    except Exception as erro:
        historico.pop()
        print(f"Não foi possível consultar a API: {erro}")
