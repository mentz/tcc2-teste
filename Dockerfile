# Contêiner Ubuntu com iperf3 para testes de baseline (calibração) para TCC
FROM  ubuntu:19.10
LABEL Description="Imagem para testes de redes em contêineres" Version="0.0.4"
RUN   apt-get update && apt-get install -y iperf3 sockperf
