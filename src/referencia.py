import time
import config
import utils

def rodar_host(dh1, dh2, logMount):
  # iPerf TCP
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
  c2.reload()
  while c2.status != 'exited':
    # print('Status c2: %s' % c2.status)
    time.sleep(1)
    c2.reload()
  
  # Encerrar e eliminar contêineres
  c1.kill()
  c1.remove()
  c2.remove()
  
  #############################################################################
  # iPerf UDP
  