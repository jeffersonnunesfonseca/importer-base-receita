import eventlet
eventlet.monkey_patch()

import fire

path_to_zips = "/home/jefferson/Pessoal/base-cnpj/"

from  importer_base_receita import importer

def run_process_socio():
    action = importer.ProcessFile()
    action.path_to_zip = path_to_zips
    action.process_socio()

def run_estabelecimento():
    action = importer.ProcessFile()
    action.path_to_zip = path_to_zips
    action.process_estabelecimento()
    
    
def run_process_empresa():
    action = importer.ProcessFile()
    action.path_to_zip = path_to_zips
    action.process_empresa()
    
if __name__ == "__main__":
    fire.Fire()