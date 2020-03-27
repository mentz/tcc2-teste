import docker
import referencia as Referencia
import interferencia as Interferencia
# import concorrencia as Concorrencia
# import trafegoDc as TrafegoDc

# Teste Referência
def referencia(driver, cfgIndex, cfg, logDir):
  if driver == 'host':
    Referencia.rodar_host(cfg[0], cfg[1], logDir)
  elif driver == 'bridge':
    if (cfgIndex == 1):
      Referencia.rodar_bridge_cfg1(cfg[0], cfg[1], logDir)
    else:
      Referencia.rodar_bridge_cfg23(cfg[0], cfg[1], logDir)
  elif driver == 'macvlan':
    Referencia.rodar_macvlan(cfg[0], cfg[1], logDir)
  elif driver == 'overlay':
    Referencia.rodar_overlay(cfg[0], cfg[1], logDir)


# Teste Referência
def interferencia(driver, cfgIndex, cfg, logDir):  
  if driver == 'host':
    Interferencia.rodar_host(cfg[0], cfg[1], cfg[2], logDir)
  elif driver == 'bridge':
    if (cfgIndex == 1):
      Interferencia.rodar_bridge_cfg1(cfg[0], cfg[1], cfg[2], logDir)
    else:
      Interferencia.rodar_bridge_cfg23(cfg[0], cfg[1], cfg[2], logDir)
  elif driver == 'macvlan':
    Interferencia.rodar_macvlan(cfg[0], cfg[1], cfg[2], logDir)
  elif driver == 'overlay':
    Interferencia.rodar_overlay(cfg[0], cfg[1], cfg[2], logDir)