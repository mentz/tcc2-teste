import time
import config
from utils import timePrint, waitThenCleanup3


def rodar_host(cliente, servidor, interferencia, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="iperf3 -s -p 5201",
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
      % (config.testDuration, servidor.ipAddr),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf TCP [DONE]")

  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="iperf3 -s -p 5202",
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
      % (config.testDuration, servidor.ipAddr),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf UDP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf server -p 11111 --tcp",
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
      % (servidor.ipAddr, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong TCP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf server -p 11111",
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
      % (servidor.ipAddr, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong UDP [DONE]")


def rodar_bridge_cfg1(cliente, servidor, interferencia, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="iperf3 -s -p 5201",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
      % (config.testDuration, c1_ip),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf TCP [DONE]")

  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="iperf3 -s -p 5202",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
      % (config.testDuration, c1_ip),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf UDP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="sockperf server -p 11111 --tcp",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
      % (c1_ip, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong TCP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="sockperf server -p 11111",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
      % (c1_ip, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong UDP [DONE]")


def rodar_bridge_cfg23(cliente, servidor, interferencia, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="iperf3 -s -p 5201",
      ports={'5201/tcp': 5201},
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_bridge,
      command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
      % (config.testDuration, servidor.ipAddr),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf TCP [DONE]")

  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="iperf3 -s -p 5202",
      ports={'5202/udp': 5202},
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
      % (config.testDuration, servidor.ipAddr),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf UDP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf server -p 11111 --tcp",
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
      % (servidor.ipAddr, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong TCP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf server -p 11111",
      detach=True)

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network="host",
      command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
      % (servidor.ipAddr, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong UDP [DONE]")



def rodar_macvlan(cliente, servidor, interferencia, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="iperf3 -s -p 5201",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
      % (config.testDuration, c1_ip),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf TCP [DONE]")

  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="iperf3 -s -p 5202",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
      % (config.testDuration, c1_ip),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf UDP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="sockperf server -p 11111 --tcp",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
      % (c1_ip, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong TCP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="sockperf server -p 11111",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_macvlan,
      command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
      % (c1_ip, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong UDP [DONE]")



def rodar_overlay(cliente, servidor, interferencia, logDir):
  #############################################################################
  # iPerf TCP
  timePrint("iPerf TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="iperf3 -s -p 5201",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
      % (config.testDuration, c1_ip),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf TCP [DONE]")

  #############################################################################
  # iPerf UDP
  timePrint("iPerf UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="iperf3 -s -p 5202",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
      % (config.testDuration, c1_ip),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  # time.sleep(config.testDuration)
  waitThenCleanup3(c2, c1, hog)
  timePrint("iPerf UDP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong TCP
  timePrint("SockPerf Ping-Pong TCP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="sockperf server -p 11111 --tcp",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="sockperf pp -i %s -t %d --mps=100 --tcp -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_tcp.csv"
      % (c1_ip, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong TCP [DONE]")

  #############################################################################
  # SockPerf Ping-Pong UDP
  timePrint("SockPerf Ping-Pong UDP [STARTING]")
  hog = interferencia.docker.containers.run(
      image="mentz/tcc:latest",
      network='none',
      command="stress-ng --cpu 2 -t %d" % (config.testDuration * 2),
      detach=True)

  c1 = servidor.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="sockperf server -p 11111",
      detach=True)
  # Obter endereço IP do contêiner
  c1_inspect = servidor.docker.api.inspect_container(c1.id)
  c1_ip = c1_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']

  c2 = cliente.docker.containers.run(
      image="mentz/tcc:latest",
      network=config.nwName_overlay,
      command="sockperf pp -i %s -t %d --mps=100 -p 11111 --full-rtt --full-log /mnt/log/sockperf_pp_udp.csv"
      % (c1_ip, config.testDuration),
      volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
      detach=True)

  # Aguardar encerramento do teste
  waitThenCleanup3(c2, c1, hog)
  timePrint("SockPerf Ping-Pong UDP [DONE]")
