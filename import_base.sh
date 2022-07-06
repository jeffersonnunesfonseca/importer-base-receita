# !/bin/bash

nohup python /home/jefferson/Pessoal/base-cnpj/importer-base-receita/run.py run_estabelecimento > /tmp/run_estabelecimento.log &
nohup python /home/jefferson/Pessoal/base-cnpj/importer-base-receita/run.py run_process_socio > /tmp/run_process_socio.log &
nohup python /home/jefferson/Pessoal/base-cnpj/importer-base-receita/run.py run_process_empresa > /tmp/run_process_empresa.log &