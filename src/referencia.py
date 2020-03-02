import time
import config
from utils import timePrint

def rodar_host(dh1, dh2, logMount):
  #############################################################################
  # iPerf TCP
  timePrint("Iniciando teste iPerf TCP")
  c1 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -s -p 5201",
        detach=True)
  
  c2 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -i 1 -t %d -c %s -p 5201 -J --logfile /mnt/log/iperf3_tcp.json"
          % (config.iperfTestDuration, dh1.ipAddr),
        mounts=[logMount],
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("Encerrando teste iPerf TCP")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  del(c1)
  del(c2)
  
  #############################################################################
  # iPerf UDP
  timePrint("Iniciando teste iPerf UDP")
  c1 = dh1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -s -p 5202",
        detach=True)
  
  c2 = dh2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="iperf3 -i 1 -b 0 -t %d -c %s -p 5202 -J --logfile /mnt/log/iperf3_udp.json"
          % (config.iperfTestDuration, dh1.ipAddr),
        mounts=[logMount],
        detach=True)
  
  # Aguardar encerramento do teste
  time.sleep(config.iperfTestDuration)
  c2.reload()
  while c2.status != 'exited':
    time.sleep(1)
    c2.reload()
  timePrint("Encerrando teste iPerf UDP")
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  del(c1)
  del(c2)
  
  
  #############################################################################
  # SockPerf Ping-Pong
  # TODO Fazer funcionar sockperf
  # timePrint("Iniciando teste SockPerf Ping-Pong")
  # c1 = dh1.docker.containers.run(
  #       image="mentz/tcc:latest",
  #       network="host",
  #       command="sockperf sr -p 11111",
  #       detach=True)
  
  # c2 = dh2.docker.containers.run(
  #       image="mentz/tcc:latest",
  #       network="host",
  #       command="sockperf -i %s -p 11111"
  #         % (config.sockperfTestDuration, dh1.ipAddr),
  #       mounts=[logMount],
  #       detach=True)
  
  # # Aguardar encerramento do teste
  # time.sleep(config.sockperfTestDuration)
  # c2.reload()
  # while c2.status != 'exited':
  #   time.sleep(1)
  #   c2.reload()
  # timePrint("Encerrando teste SockPerf Ping-Pong")
  
  # # Encerrar e eliminar contêineres
  # c1.kill()
  # c1.remove()
  # c2.remove()
  # del(c1)
  # del(c2)