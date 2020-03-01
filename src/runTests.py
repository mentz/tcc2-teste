import docker
import config
import rotinas
import utils
import os
from pathlib import Path

class DockerHost:
  def __init__(self, ipAddr):
    self.ipAddr = ipAddr
    self.docker = docker.DockerClient(base_url='tcp://%s:2376' % ipAddr)

# Definição de clientes Docker (controle dos hosts Docker, um em cada VM)
# Documentação em https://docker-py.readthedocs.io/en/stable/client.html
dh1 = DockerHost(config.h1vm1)
dh2 = DockerHost(config.h1vm2)
dh3 = DockerHost(config.h1vm3)
dh4 = DockerHost(config.h1vm4)
dh5 = DockerHost(config.h2vm1)
dh6 = DockerHost(config.h2vm2)
dhList = [dh1, dh2, dh3, dh4, dh5, dh6]

# Definições de variáveis para testes
# drivers = ['host', 'bridge', 'macvlan', 'overlay']
drivers = ['host']
cfg1 = [dh1, dh1, dh1, dh1]
cfg2 = [dh1, dh2, dh3, dh4]
cfg3 = [dh1, dh5, dh2, dh6]
cfg4 = [dh1, dh1, dh2, dh5]
# configuracoes = [cfg1, cfg2, cfg3, cfg4]
configuracoes = [cfg1]

# Limpeza dos Docker Hosts
for host in dhList:
  # Remover contêineres
  utils.purgeContainers(host.docker)
  # Remover redes de usuário
  utils.purgeUserNetworks(host.docker)

# Preparação dos Docker Hosts (criação de redes)
for host in dhList:
  # Rede Bridge
  host.docker.networks.create(name='tcc-bridge', driver='bridge')
  # Rede Macvlan
  host.docker.networks.create(name='tcc-macvlan', driver='macvlan')

# Scripts para usar como referência
# https://github.com/uktrade/docker-overlay-network-benchmark/tree/master/scripts
# https://web.archive.org/web/20171021041334/http://www.mustafaak.in/2015/12/05/docker-overlay-performance.html

# Definir diretório corrente para criar Mounts de logs das execuções
curDir = os.getcwd()

for iteracao in range(20):
  for driver in drivers:
    for (cfgIndex, cfg) in enumerate(configuracoes, start=1):
      # Somente o teste Tráfego de DC usa a quarta configuração
      if (cfg != cfg4):
        # Teste Referência
        print("--------------------------------------------")
        print("REFERENCIA   , DRIVER %7s, CFG %d, ITERACAO %2d" % (driver, cfgIndex, iteracao))
        logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'referencia', driver, cfgIndex, iteracao)
        Path(logDir).mkdir(parents=True, exist_ok=True)
        rotinas.referencia(driver, cfg, logDir)
        
      #   # Teste Interferência
      #   print("--------------------------------------------")
      #   print("INTERFERENCIA, DRIVER %7s, CFG %d, ITERACAO %2d" % (driver, cfgIndex, iteracao))
      #   logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'referencia', driver, cfgIndex, iteracao)
      #   Path(logDir).mkdir(parents=True, exist_ok=True)
      #   rotinas.interferencia(driver, cfg, logDir)
        
      #   # Teste Concorrência
      #   print("--------------------------------------------")
      #   print("CONCORRENCIA , DRIVER %7s, CFG %d, ITERACAO %2d" % (driver, cfgIndex, iteracao))
      #   logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'referencia', driver, cfgIndex, iteracao)
      #   Path(logDir).mkdir(parents=True, exist_ok=True)
      #   rotinas.concorrencia(driver, cfg, logDir)

      # # Somente o teste Tráfego de DC usa a quarta configuração
      # else:
      #   # Teste Tráfego de DC
      #   print("--------------------------------------------")
      #   print("TRAFEGODC    , DRIVER %7s, CFG %d, ITERACAO %2d" % (driver, cfgIndex, iteracao))
      #   logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'trafegoDC', driver, cfgIndex, iteracao)
      #   Path(logDir).mkdir(parents=True, exist_ok=True)
      #   rotinas.trafegoDC(driver, cfg, logDir)
