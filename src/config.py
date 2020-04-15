# Os parâmetros abaixo devem ser ajustados para conformar ao seu setup
hosts = [{'ip': '172.16.0.181', 'eth_interface': 'eth0'},
         {'ip': '172.16.0.182', 'eth_interface': 'eth0'},
         {'ip': '172.16.0.183', 'eth_interface': 'eth0'},
         {'ip': '172.16.0.184', 'eth_interface': 'eth0'},
         {'ip': '172.16.0.185', 'eth_interface': 'eth0'},
         {'ip': '172.16.0.186', 'eth_interface': 'eth0'}]

# Os parâmetros abaixo modificam as variáveis dos testes
iteracoes = 20
testDuration = 5
bgBefore = 5
bgAfter = 5

###
# Evite fazer modificações além daqui
###
import docker

nwName_bridge = 'tcc-bridge'
nwName_macvlan = 'tcc-macvlan'
nwName_overlay = 'tcc-overlay'

# Configuração para as redes macvlan - uma para cada host
ipam_pool1 = docker.types.IPAMPool(
    subnet='124.42.0.0/24',
    iprange='124.42.0.0/28',
    gateway='124.42.0.254'
  )
ipam_pool2 = docker.types.IPAMPool(
    subnet='124.42.0.0/24',
    iprange='124.42.0.16/28',
    gateway='124.42.0.254'
  )
ipam_pool3 = docker.types.IPAMPool(
    subnet='124.42.0.0/24',
    iprange='124.42.0.32/28',
    gateway='124.42.0.254'
  )
ipam_pool4 = docker.types.IPAMPool(
    subnet='124.42.0.0/24',
    iprange='124.42.0.48/28',
    gateway='124.42.0.254'
  )
ipam_pool5 = docker.types.IPAMPool(
    subnet='124.42.0.0/24',
    iprange='124.42.0.64/28',
    gateway='124.42.0.254'
  )
ipam_pool6 = docker.types.IPAMPool(
    subnet='124.42.0.0/24',
    iprange='124.42.0.80/28',
    gateway='124.42.0.254'
  )

ipam_config1 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool1]
  )
ipam_config2 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool2]
  )
ipam_config3 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool3]
  )
ipam_config4 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool4]
  )
ipam_config5 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool5]
  )
ipam_config6 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool6]
  )

ipam_config = [
  ipam_config1,
  ipam_config2,
  ipam_config3,
  ipam_config4,
  ipam_config5,
  ipam_config6,
]