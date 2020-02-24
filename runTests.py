import docker
from '.\config' import config

# Definição de clientes Docker
# Documentação em https://docker-py.readthedocs.io/en/stable/client.html
# c1: nó físico 1, vm 1
# c2: nó físico 1, vm 2
# c3: nó físico 2, vm 1
c1 = docker.DockerClient(base_url="tcp://docker1-1:2375")
c2 = docker.DockerClient(base_url="tcp://docker1-2:2375")
c3 = docker.DockerClient(base_url="tcp://docker2-1:2375")

drivers = ['host', 'bridge', 'macvlan', 'overlay']
cenarios = ['referencia', 'interferencia', 'concorrencia']
cenario4 = 'nuvem'