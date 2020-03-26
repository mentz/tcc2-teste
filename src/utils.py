import time

def purgeContainers(dockerClient):
  # Remover contêineres
  for ct in dockerClient.containers.list(all=True):
    ct.remove(force=True)

def purgeUserNetworks(dockerClient):
  # Remover redes de usuário
  dockerClient.networks.prune()
  
def timePrint(string):
  now = time.localtime()
  print('[%4d-%02d-%02d %2d:%02d:%02d] %s' %
        (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min,
         now.tm_sec, string))

def waitThenCleanup(client, server):
  client.reload()
  while client.status != 'exited':
    time.sleep(1)
    client.reload()
  # Encerrar e eliminar contêineres
  server.kill()
  server.remove()
  client.remove()