# Contêiner Ubuntu com ferramentas de testes de rede para meu TCC
FROM  ubuntu:19.10
LABEL Description="Imagem com ferramentas usadas no meu TCC" Version="1.0.0"
RUN   apt-get update && apt-get install -y iperf3 sockperf stress-ng
COPY  ./src/etg/etg-client ./src/etg/etg-server ./src/etg/PRV2_1_CDF /root/