import docker
import referencia as Referencia
# import interferencia as Interferencia
# import concorrencia as Concorrencia
# import trafegoDc as TrafegoDc

# Teste Referência
def referencia(driver, cfg, logDir):
  logMount = docker.types.Mount(
              target='/mnt/log',
              source=logDir,
              type='bind')
  
  if driver == 'host':
    Referencia.rodar_host(cfg[0], cfg[1], logMount)