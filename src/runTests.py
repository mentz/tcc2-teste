import docker
import config
import rotinas

# Definição de clientes Docker (controle dos hosts Docker, um em cada VM)
# Documentação em https://docker-py.readthedocs.io/en/stable/client.html
h1vm1 = docker.DockerClient(base_url='tcp://%s:2376' % config.h1vm1)
h1vm2 = docker.DockerClient(base_url='tcp://%s:2376' % config.h1vm2)
h1vm3 = docker.DockerClient(base_url='tcp://%s:2376' % config.h1vm3)
h1vm4 = docker.DockerClient(base_url='tcp://%s:2376' % config.h1vm4)
h2vm1 = docker.DockerClient(base_url='tcp://%s:2376' % config.h2vm1)
h2vm2 = docker.DockerClient(base_url='tcp://%s:2376' % config.h2vm2)
hosts = [h1vm1, h1vm2, h1vm3, h1vm4, h2vm1, h2vm2]

# Limpeza dos Docker Hosts
for host in hosts:
  # Remover contêineres
  for ct in host.containers.list():
    host.api.remove_container(ct.id, force=True)
  # Remover redes de usuário
  host.networks.prune()



# Definições de testes
drivers = ['host', 'bridge', 'macvlan', 'overlay']
configuracoes = [1, 2, 3, 4]

# Scripts para usar como referência
# https://github.com/uktrade/docker-overlay-network-benchmark/tree/master/scripts
# https://web.archive.org/web/20171021041334/http://www.mustafaak.in/2015/12/05/docker-overlay-performance.html


# Nova ideia: fazer rodar no terminal, copiar os comandos para o Python.
