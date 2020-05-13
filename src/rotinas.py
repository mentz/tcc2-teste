import docker
import referencia as Referencia
import interferencia as Interferencia
import concorrencia as Concorrencia
# import trafegoDC as TrafegoDC


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


# Teste Interferência
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


# Teste Concorrência
def concorrencia(driver, cfgIndex, cfg, logDir):
  if driver == 'host':
    Concorrencia.rodar_host(cfg[0], cfg[1], cfg[2], cfg[3], logDir)
  elif driver == 'bridge':
    if (cfgIndex == 1):
      Concorrencia.rodar_bridge_cfg1(
          cfg[0], cfg[1], cfg[2], cfg[3], logDir)
    else:
      Concorrencia.rodar_bridge_cfg23(
          cfg[0], cfg[1], cfg[2], cfg[3], logDir)
  elif driver == 'macvlan':
    Concorrencia.rodar_macvlan(cfg[0], cfg[1], cfg[2], cfg[3], logDir)
  elif driver == 'overlay':
    Concorrencia.rodar_overlay(cfg[0], cfg[1], cfg[2], cfg[3], logDir)
