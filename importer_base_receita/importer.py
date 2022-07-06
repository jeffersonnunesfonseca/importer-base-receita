import os
import eventlet
import pandas as pd
from importer_base_receita.base import FileProcessor
from importer_base_receita import db_engine

class ProcessFile(FileProcessor):
    
    path_to_zip = None # caminho para os arquivos
    CHUNK_SIZE = 200
    def __init__(self) -> None:
        super().__init__()
        
        self._types = [
            "empresa",
            "estabelecimento",
            "socio"
        ]
        self.query_pool = eventlet.GreenPool(100) # executa X queries paralelas

    def execute(self):
        print("Preparando arquivos ...")
        self.prepare_files()
        
        print("Iniciando processamento em massa")       
        
        for type in self._types:
            print(f"spawmando {type}")     
            self.query_pool.spawn(self._spawn, type)

        # total_empresas = self.process_empresa()
        self.query_pool.waitall()

    
    def _spawn(self, type):
        if type == "empresa":        
            self.process_empresa()
        elif type == "socio":
            self.process_socio()
        elif type == "estabelecimento":
            self.process_estabelecimento()
            
    def process_empresa(self):
        processed_items = 0
        files = os.listdir(f"{self._workspace}empresa/")
        total_files = len(files)
        cont_file = 1
        for file in files:
            print(f"Total de arquivos = {total_files}, arquivo atual [{cont_file}] - {file}")
            file = f"{self._workspace}empresa/{file}"            
            csv = pd.read_csv(
                file,
                sep=';',
                encoding='ISO-8859-1',
                chunksize=self.CHUNK_SIZE,
                header=None,
                names=['cnpj_basico','razao_social','natureza_juridica','qualificacao_responsavel','capital_social','porte_empresa','ente_federativo_responsavel'],
                error_bad_lines=False,
                dtype=str
            )

            df = next(csv)

            # buffer da planilha
            while df is not None:
                try:
                    next_df = next(csv)
                except StopIteration:
                    next_df = None
   
                df.to_sql('empresa', con=db_engine, if_exists='append', index=False, chunksize=self.CHUNK_SIZE, index_label='id', method='multi')
                processed_items += (len(df))
                print(f"Qtd empresas processadas até o momento do arquivo {cont_file}: {processed_items}")
                df = next_df
            
            cont_file += 1
            print("\n")
                    
        return processed_items
    
    def process_socio(self):
        processed_items = 0
        files = os.listdir(f"{self._workspace}socio/")
        total_files = len(files)
        cont_file = 1
         
        for file in files:
            print(f"Total de arquivos = {total_files}, arquivo atual [{cont_file}] - {file}")
            file = f"{self._workspace}socio/{file}"            
            csv = pd.read_csv(
                file,
                sep=';',
                encoding='ISO-8859-1',
                chunksize=self.CHUNK_SIZE,
                header=None,
                names=['cnpj_basico', 'identificador_socio', 'nome', 'cpf_cnpj', 'qualificacao_socio', 'data_entrada_sociedade', 'pais', 'representante_legal', 'nome_representante', 'qualificacao_representante', 'faixa_etaria'],
                error_bad_lines=False,
                dtype=str
            )

            df = next(csv)

            # buffer da planilha
            while df is not None:
                try:
                    next_df = next(csv)
                except StopIteration:
                    next_df = None
   
                df.to_sql('socio', con=db_engine, if_exists='append', index=False, chunksize=self.CHUNK_SIZE, index_label='id', method='multi')
                processed_items += (len(df))
                print(f"Qtd socios processados até o momento do arquivo {cont_file}: {processed_items}")
                df = next_df
            
            cont_file += 1
            print("\n")
                    
        return processed_items
    
    def process_estabelecimento(self):
        processed_items = 0
        files = os.listdir(f"{self._workspace}estabelecimento/")
        total_files = len(files)
        cont_file = 1
        cols =[
            'cnpj_basico',
            'cnpj_ordem',
            'cnpj_dv',
            'qualificacao_responsavel',
            'identificador_matriz_filial',
            'nome_fantasia',
            'situacao_cadastral',
            'data_situacao_cadastral',
            'motivo_situacao_cadastral',
            'nome_cidade_exterior',
            'pais',
            'data_inicio_atividade',
            'cnae_principal',
            'cnae_secundario',
            'tipo_logradouro',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cep',
            'uf',
            'municipio',
            'ddd_1',
            'telefone_1',
            'ddd_2',
            'telefone_2',
            'ddd_fax',
            'fax',
            'correio_eletronico',
            'situacao_especial',
            'data_situacao_especial'
        ]
        for file in files:
            print(f"Total de arquivos = {total_files}, arquivo atual [{cont_file}] - {file}")
            file = f"{self._workspace}estabelecimento/{file}"            
            csv = pd.read_csv(
                file,
                sep=';',
                encoding='ISO-8859-1',
                chunksize=self.CHUNK_SIZE,
                header=None,
                names=cols,
                error_bad_lines=False,
                dtype=str
            )

            df = next(csv)

            # buffer da planilha
            while df is not None:
                try:
                    next_df = next(csv)
                except StopIteration:
                    next_df = None
   
                df.to_sql('estabelecimento', con=db_engine, if_exists='append', index=False, chunksize=self.CHUNK_SIZE, index_label='id', method='multi')
                processed_items += (len(df))
                print(f"Qtd estabelecimentos processados até o momento do arquivo {cont_file}: {processed_items}")
                df = next_df
            
            cont_file += 1
            print("\n")
                    
        return processed_items
    
    def prepare_files(self):
        if not os.path.exists(self._workspace):
            self.create_folder(self._workspace)
            
        for type in self._types:
            original_path = f"{self.path_to_zip}{type}"
            if not os.path.exists(f"{original_path}{type}"):
                print(f"Diretorio nao existe {original_path}")
            
            tmp_path = f"{self._workspace}{type}"
            if not os.path.exists(tmp_path):
                self.create_folder(tmp_path)
                for file in os.listdir(original_path):
                    unziped = self.unzip(original_path + "/" + file, tmp_path)
                    print(unziped)