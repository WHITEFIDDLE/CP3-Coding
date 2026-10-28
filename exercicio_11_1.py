import docker


cliente = docker.from_env()
containers = cliente.containers.list(all=True)

print(f"{'NOME':<20} {'STATUS':<12} IMAGEM")

for container in containers:
    imagens = container.image.tags
    imagem = imagens[0] if imagens else container.image.short_id
    aviso = " <- PARADO" if container.status != "running" else ""

    print(
        f"{container.name:<20} "
        f"{container.status:<12} "
        f"{imagem}{aviso}"
    )

rodando = sum(
    container.status == "running"
    for container in containers
)

print(f"\nTotal: {len(containers)}")
print(f"Rodando: {rodando}")
print(f"Parados: {len(containers) - rodando}")
