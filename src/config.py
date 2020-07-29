# Os parâmetros abaixo devem ser ajustados para conformar ao seu setup
import docker
hosts = [{'ip': '10.11.10.92', 'eth_interface': 'ens3'},
         {'ip': '10.11.13.191', 'eth_interface': 'ens3'},
         {'ip': '10.11.13.77', 'eth_interface': 'ens3'},
         {'ip': '10.11.10.158', 'eth_interface': 'ens3'},
         {'ip': '10.11.13.82', 'eth_interface': 'ens3'},
         {'ip': '10.11.10.170', 'eth_interface': 'ens3'}]

# Os parâmetros abaixo modificam as variáveis dos testes
iteracoes = 20
testDuration = 120
bgBefore = 10
bgAfter = 10

etgClientSeed = "1109835023"
etgConfigDefault = """server {} 5000
server {} 5000
server {} 5000
req_size_dist /root/PRV2_1_CDF
fanout 1 100
load 1000Mbps
num_reqs 250000"""
etgTestCommand = """bash -c '{{
cat <<HERE
{}
HERE
}} | tee /root/etgConfig
{{ time /root/etg-client -c /root/etgConfig -s {}; }} > etgrun.log 2> run_time.log
mv etgrun.log run_time.log log_flows.out log_reqs.out /mnt/log/.'
"""

###
# Evite fazer modificações além daqui
###

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
