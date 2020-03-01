def purgeContainers(dockerClient):
  # Remover contêineres
  for ct in dockerClient.containers.list(all=True):
    ct.remove(force=True)

def purgeUserNetworks(dockerClient):
  # Remover redes de usuário
  dockerClient.networks.prune()