import docker
import config
from rotinas import referencia#, interferencia, concorrencia, trafegoDC

# Definição de clientes Docker (controle dos hosts Docker, um em cada VM)
# Documentação em https://docker-py.readthedocs.io/en/stable/client.html
h1vm1 = docker.DockerClient(base_url=config.h1vm1)
h1vm2 = docker.DockerClient(base_url=config.h1vm2)
h1vm3 = docker.DockerClient(base_url=config.h1vm3)
h1vm4 = docker.DockerClient(base_url=config.h1vm4)
h2vm1 = docker.DockerClient(base_url=config.h2vm1)
h2vm2 = docker.DockerClient(base_url=config.h2vm2)
hosts = [h1vm1, h1vm2, h1vm3, h1vm4, h2vm1, h2vm2]

drivers = ['host', 'bridge', 'macvlan', 'overlay']
configuracoes = [1, 2, 3, 4]

for configuracao in configuracoes:
  for driver in drivers:
    if configuracao == 'referencia':
      # criar rede usando o driver da vez
      referencia(configuracao, driver, hosts)
      # remover a rede criada