#!/bin/sh

arg=${1-normal}

if test ! -e './results' -o $arg = '-f'
then
  echo 'Iniciando script...'
  rm -rf 'results'
  mkdir 'results'
  python3 src/runTests.py
else
  echo 'Já existem resultados de outra execução.'
  echo 'Renomeie a pasta "results" para outro nome e rode novamente, ou use o'
  echo ' argumento "-f" para forçar a execução (Obs.: remove os resultados'
  echo ' anteriores).'
fi
