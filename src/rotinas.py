# Teste Referência, Configuração QUALQUER, Driver host
def testeReferencia_1234_host(dh1, dh2, ip1, logMount):
  c1 = dh1.containers.create(image="mentz/tcc:latest", network="host", command="iperf3 -s -p 8375")
  c2 = dh2.containers.create(image="mentz/tcc:latest", network="host", command="iperf3 -c %s -p 8375" % ip1)
  
# Teste Referência, Configuração 1, Driver bridge
# Teste Referência, Configuração 1, Driver macvlan
# Teste Referência, Configuração 1, Driver overlay