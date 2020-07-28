import time
import config
from utils import timePrint, waitThenCleanup


def rodar_host(cliente, servidor1, servidor2, servidor3, logDir):
    #############################################################################
    # TrafegoDC
    timePrint("TrafegoDC [STARTING]")
    s1 = servidor1.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="/root/etg-server",
        detach=True)

    s2 = servidor2.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="/root/etg-server",
        detach=True)

    s3 = servidor3.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="/root/etg-server",
        detach=True)

    etgConfig = config.etgConfigDefault.format(
        servidor1.ipAddr, servidor2.ipAddr, servidor3.ipAddr)
    print(etgConfig)
    return

    c1 = cliente.docker.containers.run(
        image="mentz/tcc:latest",
        network="host",
        command="cat <<EOF\
			{}\
			EOF >> /root/etgConfig;\
			/root/etg-client -c /root/etgConfig / -log host;\
			mv /root/*.out /mnt/log/.".format(etgConfig),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)

    # Aguardar encerramento do teste
    # time.sleep(config.testDuration)
    waitThenCleanup(c1, s1, s2, s3)
    timePrint("TrafegoDC [DONE]")


def rodar_bridge(cliente, servidor1, servidor2, servidor3, logDir):
    #############################################################################
    # TrafegoDC
    timePrint("TrafegoDC [STARTING]")
    s1 = servidor1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="/root/etg-server",
        detach=True)

    s2 = servidor2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="/root/etg-server",
        ports={'5000/tcp': 5000},
        detach=True)

    s3 = servidor3.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="/root/etg-server",
        ports={'5000/tcp': 5000},
        detach=True)

    # Obter endereço IP do contêiner co-hospedado (s1)
    s1_inspect = servidor.docker.api.inspect_container(s1.id)
    s1_ip = s1_inspect['NetworkSettings']['Networks'][config.nwName_bridge]['IPAddress']

    etgConfig = config.etgConfigDefault.format(
        s1_ip, servidor2.ipAddr, servidor3.ipAddr)
    print(etgConfig)
    return

    c1 = cliente.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_bridge,
        command="cat <<EOF\
			{}\
			EOF >> /root/etgConfig;\
			/root/etg-client -c /root/etgConfig / -log host;\
			mv /root/*.out /mnt/log/.".format(etgConfig),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)

    # Aguardar encerramento do teste
    # time.sleep(config.testDuration)
    waitThenCleanup(c1, s1, s2, s3)
    timePrint("TrafegoDC [DONE]")


def rodar_macvlan(cliente, servidor1, servidor2, servidor3, logDir):
    #############################################################################
    # TrafegoDC
    timePrint("TrafegoDC [STARTING]")
    s1 = servidor1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_macvlan,
        command="/root/etg-server",
        detach=True)

    s2 = servidor2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_macvlan,
        command="/root/etg-server",
        detach=True)

    s3 = servidor3.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_macvlan,
        command="/root/etg-server",
        detach=True)

    # Obter endereço IP dos contêineres na MacVLan
    s1_inspect = servidor.docker.api.inspect_container(s1.id)
    s1_ip = s1_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']
    s2_inspect = servidor.docker.api.inspect_container(s2.id)
    s2_ip = s2_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']
    s3_inspect = servidor.docker.api.inspect_container(s3.id)
    s3_ip = s3_inspect['NetworkSettings']['Networks'][config.nwName_macvlan]['IPAddress']

    etgConfig = config.etgConfigDefault.format(s1_ip, s2_ip, s3_ip)
    print(etgConfig)
    return

    c1 = cliente.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_macvlan,
        command="cat <<EOF\
			{}\
			EOF >> /root/etgConfig;\
			/root/etg-client -c /root/etgConfig / -log host;\
			mv /root/*.out /mnt/log/.".format(etgConfig),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)

    # Aguardar encerramento do teste
    # time.sleep(config.testDuration)
    waitThenCleanup(c1, s1, s2, s3)
    timePrint("TrafegoDC [DONE]")


def rodar_overlay(cliente, servidor1, servidor2, servidor3, logDir):
    #############################################################################
    # TrafegoDC
    timePrint("TrafegoDC [STARTING]")
    s1 = servidor1.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_overlay,
        command="/root/etg-server",
        detach=True)

    s2 = servidor2.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_overlay,
        command="/root/etg-server",
        detach=True)

    s3 = servidor3.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_overlay,
        command="/root/etg-server",
        detach=True)

    # Obter endereço IP dos contêineres na MacVLan
    s1_inspect = servidor.docker.api.inspect_container(s1.id)
    s1_ip = s1_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']
    s2_inspect = servidor.docker.api.inspect_container(s2.id)
    s2_ip = s2_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']
    s3_inspect = servidor.docker.api.inspect_container(s3.id)
    s3_ip = s3_inspect['NetworkSettings']['Networks'][config.nwName_overlay]['IPAddress']

    etgConfig = config.etgConfigDefault.format(s1_ip, s2_ip, s3_ip)
    print(etgConfig)
    return

    c1 = cliente.docker.containers.run(
        image="mentz/tcc:latest",
        network=config.nwName_overlay,
        command="cat <<EOF\
			{}\
			EOF >> /root/etgConfig;\
			/root/etg-client -c /root/etgConfig / -log host;\
			mv /root/*.out /mnt/log/.".format(etgConfig),
        volumes={logDir: {'bind': '/mnt/log', 'mode': 'rw'}},
        detach=True)

    # Aguardar encerramento do teste
    # time.sleep(config.testDuration)
    waitThenCleanup(c1, s1, s2, s3)
    timePrint("TrafegoDC [DONE]")
