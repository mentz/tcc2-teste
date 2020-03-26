import docker
import referencia as Referencia
# import interferencia as Interferencia
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