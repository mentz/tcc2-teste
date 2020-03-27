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
dh1 = DockerHost(config.hosts[0]['ip'])
dh2 = DockerHost(config.hosts[1]['ip'])
dh3 = DockerHost(config.hosts[2]['ip'])
dh4 = DockerHost(config.hosts[3]['ip'])
dh5 = DockerHost(config.hosts[4]['ip'])
dh6 = DockerHost(config.hosts[5]['ip'])
dhList = [dh1, dh2, dh3, dh4, dh5, dh6]

# Definições de variáveis para testes
drivers = ['host', 'bridge', 'macvlan', 'overlay']
cfg1 = [dh1, dh1, dh1, dh1]
cfg2 = [dh1, dh2, dh3, dh4]
cfg3 = [dh1, dh5, dh2, dh6]
cfg4 = [dh1, dh1, dh2, dh5]
# configuracoes = [cfg1, cfg2, cfg3, cfg4]
configuracoes = [cfg1, cfg2, cfg3]

# Limpeza dos Docker Hosts
for host in dhList:
  # Remover contêineres
  utils.purgeContainers(host.docker)
  # Remover redes de usuário
  utils.purgeUserNetworks(host.docker)

# Preparação dos Docker Hosts (criação de redes)
overlayExists = False
for (idx, host) in enumerate(dhList):
  bridgeExists = False
  macvlanExists = False

  # Rede Bridge
  for nw in host.docker.networks.list():
    if (nw.name == config.nwName_bridge):
      bridgeExists = True
  if (not bridgeExists):
    host.docker.networks.create(name=config.nwName_bridge, driver='bridge')

  # Rede Macvlan
  for nw in host.docker.networks.list():
    if (nw.name == config.nwName_macvlan):
      macvlanExists = True
  if (not macvlanExists):
    host.docker.networks.create(
      name=config.nwName_macvlan,
      driver='macvlan',
      ipam=config.ipam_config[idx],
      options={'parent': config.hosts[idx]['eth_interface']})

  # Rede Overlay
  for nw in host.docker.networks.list():
    if (nw.name == config.nwName_overlay):
      overlayExists = True

# Criar rede Overlay (uma para todos os hosts)
if (not overlayExists):
  dh1.docker.networks.create(
    name=config.nwName_overlay,
    driver='overlay',
    attachable=True)

# Scripts para usar como referência
# https://github.com/uktrade/docker-overlay-network-benchmark/tree/master/scripts
# https://web.archive.org/web/20171021041334/http://www.mustafaak.in/2015/12/05/docker-overlay-performance.html

# Definir diretório corrente para criar Mounts de logs das execuções
curDir = os.getcwd()

for iteracao in range(1, config.iteracoes + 1):
  for driver in drivers:
    for (cfgIndex, cfg) in enumerate(configuracoes, start=1):
      # Somente o teste Tráfego de DC usa a quarta configuração
      if (cfg != cfg4):
        # Teste Referência
        print('[REFERENCIA, DRIVER %s, CFG %d, ITERACAO %2d]' % (driver, cfgIndex, iteracao))
        logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'referencia', driver, cfgIndex, iteracao)
        rotinas.referencia(driver, cfgIndex, cfg, logDir)

        # Teste Interferência
        print('[INTERFERENCIA, DRIVER %s, CFG %d, ITERACAO %2d]' % (driver, cfgIndex, iteracao))
        logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'interferencia', driver, cfgIndex, iteracao)
        rotinas.interferencia(driver, cfgIndex, cfg, logDir)

        # Teste Concorrência
      #   print('[CONCORRENCIA, DRIVER %s, CFG %d, ITERACAO %2d]' % (driver, cfgIndex, iteracao))
        logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'concorrencia', driver, cfgIndex, iteracao)
      #   rotinas.concorrencia(driver, cfgIndex, cfg, logDir)

      # # Somente o teste Tráfego de DC usa a quarta configuração
      else:
      #   # Teste Tráfego de DC
      #   print('[TRAFEGODC, DRIVER %s, CFG %d, ITERACAO %2d]' % (driver, cfgIndex, iteracao))
        logDir = '%s/results/cenario_%s/driver_%s/cfg%d/iter%02d' % (curDir, 'trafegoDC', driver, cfgIndex, iteracao)
      #   rotinas.trafegoDC(driver, cfgIndex, cfg, logDir)
