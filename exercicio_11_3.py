import time
from datetime import datetime

import docker
from docker.errors import NotFound


cliente = docker.from_env()
nome_container = "web_lab"

for _ in range(6):
    horario = datetime.now().strftime("%H:%M:%S")

    try:
        container = cliente.containers.get(nome_container)
        container.reload()

        if container.status == "running":
            print(f"[{horario}] {nome_container}: running — OK")
        else:
            print(
                f"[{horario}] {nome_container}: {container.status} — "
                "ALERTA! Tentando reiniciar..."
            )
            container.restart()
            print(f"{nome_container} reiniciado com sucesso.")

    except NotFound:
        print(
            f"[{horario}] ALERTA: "
            f"contêiner {nome_container} não encontrado."
        )

    time.sleep(10)
