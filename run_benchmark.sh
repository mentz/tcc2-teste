#!/bin/sh

arg=${1-normal}

if test ! -e './results' -o $arg = '-f'
then
  echo 'Iniciando script...'
  rm -rf 'results'
  mkdir 'results'

  # Garantir que não há mpstat de outra execução
  for i in $(seq 1 6); do
    ssh dh-$i "killall mpstat"
  done

  # Iniciar coleta de dados dos hospedeiros
  date=$(date --iso-8601)
  for i in $(seq 1 6); do
    ssh dh-$i "mpstat -o JSON 1 > ~/mpstat_dh-${i}_${date}.json &"
  done

  # Rodar bateria de testes
  python3 src/runTests.py

  # Encerrar coleta de dados e agregar nessa pasta
  for i in $(seq 1 6); do
    ssh dh-$i "killall mpstat"
    scp dh-$i:~/mpstat_dh-${i}_${date}.json results/.
  done
else
  echo 'Já existem resultados de outra execução.'
  echo 'Renomeie a pasta "results" para outro nome e rode novamente, ou use o'
  echo ' argumento "-f" para forçar a execução (Obs.: remove os resultados'
  echo ' anteriores).'
fi
