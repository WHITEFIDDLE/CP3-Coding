import docker
import requests
from docker.errors import APIError


cliente = docker.from_env()
container = None

try:
    print("Subindo Nginx...")

    container = cliente.containers.run(
        "nginx:latest",
        name="nginx_exercicio_11_2",
        ports={"80/tcp": 8080},
        detach=True,
    )

    resposta = requests.get(
        "http://localhost:8080",
        timeout=20,
    )

    print(f"Nginx respondeu: {resposta.status_code}")

except (APIError, requests.RequestException) as erro:
    print(f"Erro ao iniciar ou acessar o Nginx: {erro}")

finally:
    if container is not None:
        print("Derrubando e removendo contêiner...")
        container.stop()
        container.remove()
        print("Concluído. Ambiente limpo.")
