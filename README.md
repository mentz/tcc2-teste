# TCC2 - Testes
Este repositório contém os scripts usados nos testes desenvolvidos no meu TCC2.

São usados até seis hospedeiros para realização dos testes.
Nada impede o uso de um número menor mas os testes não serão comparáveis.

Os scripts são feitos pensando que os hospedeiros terão nomes `dh-1` a `dh-6`.
Caso necessário adapte isso no `run_benchmark.sh` e em `src/config.py`.

Ferramentas necessárias nos hosts:
- `Docker` configurado em modo Swarm
- `sysstat` (usamos `mpstat`)
