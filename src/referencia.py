import time
import config
from utils import timePrint

def rodar_host(dh1, dh2, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -s -p 5201",
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
          % (config.iperfTestDuration, dh1.ipAddr),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("iPerf TCP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -s -p 5202",
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
          % (config.iperfTestDuration, dh1.ipAddr),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("iPerf UDP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf server -p 11111 --tcp",
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
          % (dh1.ipAddr, config.sockperfTestDuration),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("SockPerf Ping-Pong TCP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf server -p 11111",
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
          % (dh1.ipAddr, config.sockperfTestDuration),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("SockPerf Ping-Pong UDP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()



def rodar_bridge_cfg1(dh1, dh2, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="iperf3 -s -p 5201",
        detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = dh1.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
          % (config.iperfTestDuration, c1_ip),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("iPerf TCP  - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="iperf3 -s -p 5202",
        detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = dh1.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
          % (config.iperfTestDuration, c1_ip),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("iPerf UDP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf server -p 11111 --tcp",
        detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = dh1.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
          % (c1_ip, config.sockperfTestDuration),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("SockPerf Ping-Pong TCP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="sockperf server -p 11111",
        detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = dh1.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
          % (c1_ip, config.sockperfTestDuration),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("SockPerf Ping-Pong UDP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()



def rodar_bridge_cfg23(dh1, dh2, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="iperf3 -s -p 5201",
        ports={'5201/tcp': 5201},
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
          % (config.iperfTestDuration, dh1.ipAddr),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("iPerf TCP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -s -p 5202",
        ports={'5202/udp': 5202},
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
          % (config.iperfTestDuration, dh1.ipAddr),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("iPerf UDP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf server -p 11111 --tcp",
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
          % (dh1.ipAddr, config.sockperfTestDuration),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("SockPerf Ping-Pong TCP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  
  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP - [STARTING]")
  c1 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf server -p 11111",
        detach=True)
  
  c2 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
          % (dh1.ipAddr, config.sockperfTestDuration),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)
  
  # Aguardar encerramento do teste
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("SockPerf Ping-Pong UDP - [DONE]")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
 