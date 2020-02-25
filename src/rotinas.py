def referencia(configuracao, network, hosts):
  # Aceita argumentos:
  # configuracao = 1, 2, 3
  # network = (string de valor referente uma rede existente no docker)
  # hosts = (objeto contendo os controladores Docker das 4 VMs)
  h1 = hosts[0]
  h2 = hosts[1]
  h3 = hosts[2]
  h4 = hosts[3]
  if configuracao == 1:
    # subir c1 e c2, rodar testes somente com eles
    print(configuracao + ' com ' + network)
    c1 = h1.containers.create('lucas/tcc:baseline', 'iperf3 -s')
  elif configuracao == 2:
    # subir c1, c2 e c3. iperf entre c1 e c2, enquanto c3 roda stressng em cpu
    print(configuracao + ' com ' + network)
  elif configuracao == 3:
    # subir c1, c2, c3 e c4. iperf entre c1 e c2 enquanto iperf roda entre c3 e c4
    print(configuracao + ' com ' + network)
  else:
    print(configuracao + ' com ' + network + '------- ERRO, INVÁLIDO')
    return 0