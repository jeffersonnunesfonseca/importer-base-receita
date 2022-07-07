"""criando tabelas com base no layout da receita https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/arquivos/novolayoutdosdadosabertosdocnpj-dez2021.pdf

Revision ID: 71b0f62d438b
Revises: 
Create Date: 2022-07-05 13:32:18.086279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71b0f62d438b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # op.execute('CREATE SCHEMA if not exists base_cnpj;')
    create_table_empresas()
    create_table_estabelecimentos()
    create_table_socios()
    create_index()


def downgrade():
    op.drop_table("empresa")
    op.drop_table("estabelecimento")
    op.drop_table("socio")

def create_table_empresas():
    op.create_table(
        'empresa',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('cnpj_basico', sa.Integer()),
        sa.Column('razao_social', sa.String(length=300)),
        sa.Column('natureza_juridica', sa.Integer()),
        sa.Column('qualificacao_responsavel', sa.String(length=300)),
        sa.Column('capital_social', sa.DECIMAL(10,2)),
        sa.Column('porte_empresa', sa.Integer()), # A CÓDIGO DO PORTE DA EMPRESA: 00 – NÃO INFORMADO 01 - MICRO EMPRESA 03 - EMPRESA D
        sa.Column('ente_federativo_responsavel', sa.String(length=300)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),        
        sa.PrimaryKeyConstraint('id'),
    )

def create_table_estabelecimentos():
    op.create_table(
        'estabelecimento',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('cnpj_basico', sa.Integer()),
        sa.Column('cnpj_ordem', sa.Integer()),
        sa.Column('cnpj_dv', sa.Integer()),
        sa.Column('identificador_matriz_filial', sa.Integer()), #CÓDIGO DO IDENTIFICADOR MATRIZ/FILIAL: 1 – MATRIZ 2 – FILIAL
        sa.Column('nome_fantasia', sa.String(length=300)),
        sa.Column('situacao_cadastral', sa.Integer()), # CÓDIGO DA SITUAÇÃO CADASTRAL: 01 – NULA 2 – ATIVA 3 – SUSPENSA 4 – INAPTA 08 – BAIXADA
        sa.Column('data_situacao_cadastral', sa.Date()),
        sa.Column('motivo_situacao_cadastral', sa.String(length=300)),
        sa.Column('nome_cidade_exterior', sa.String(length=300)),
        sa.Column('pais', sa.String(length=300)),
        sa.Column('data_inicio_atividade', sa.Date()),
        sa.Column('cnae_principal', sa.String(length=300)),
        sa.Column('cnae_secundario', sa.String(length=300)),
        sa.Column('tipo_logradouro', sa.String(length=300)),
        sa.Column('logradouro', sa.String(length=300)),
        sa.Column('numero', sa.Integer()),
        sa.Column('complemento', sa.String(length=300)),
        sa.Column('bairro', sa.String(length=300)),
        sa.Column('cep', sa.String(length=300)),
        sa.Column('uf', sa.String(length=300)),
        sa.Column('municipio', sa.String(length=300)),
        sa.Column('ddd_1', sa.String(length=300)),
        sa.Column('telefone_1', sa.String(length=300)),
        sa.Column('ddd_2', sa.String(length=300)),
        sa.Column('telefone_2', sa.String(length=300)),
        sa.Column('ddd_fax', sa.String(length=300)),
        sa.Column('fax', sa.String(length=300)),
        sa.Column('correio_eletronico', sa.String(length=300)),
        sa.Column('situacao_especial', sa.String(length=300)),
        sa.Column('data_situacao_especial', sa.Date()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),        
        sa.PrimaryKeyConstraint('id'),
    )

def create_table_socios():
    op.create_table(
        'socio',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('cnpj_basico', sa.Integer()),
        sa.Column('identificador_socio', sa.Integer()), # CÓDIGO DO IDENTIFICADOR DE SÓCIO 1 – PESSOA JURÍDICA 2 – PESSOA FÍSICA 3 – ESTRANGEIRO
        sa.Column('nome', sa.String(length=300)),
        sa.Column('cpf_cnpj', sa.String(length=300)),
        sa.Column('qualificacao_socio', sa.String(length=300)),
        sa.Column('data_entrada_sociedade', sa.Date()),
        sa.Column('pais', sa.String(length=300)),
        sa.Column('representante_legal', sa.String(length=300)),
        sa.Column('nome_representante', sa.String(length=300)),
        sa.Column('qualificacao_representante', sa.String(length=300)),
        sa.Column('faixa_etaria', sa.String(length=300)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),        
        sa.PrimaryKeyConstraint('id'),
    )
    

def create_index():
        op.execute('CREATE INDEX idx_cnpj_basico on empresa (cnpj_basico)')
        op.execute('CREATE INDEX idx_cnpj_basico on estabelecimento (cnpj_basico)')
        op.execute('CREATE INDEX idx_cnpj_basico on socio (cnpj_basico)')
        
        op.execute('CREATE INDEX idx_natureza_juridica on empresa (natureza_juridica)')
        op.execute('CREATE INDEX idx_faixa_etaria on socio (faixa_etaria)')
        
        op.execute('CREATE INDEX idx_uf on estabelecimento (uf)')
        op.execute('CREATE INDEX idx_cnae_principal on estabelecimento (cnae_principal)')
        op.execute('CREATE INDEX idx_ddd_1 on estabelecimento (ddd_1)')
        op.execute('CREATE INDEX idx_ddd_2 on estabelecimento (ddd_2)')
        op.execute('CREATE INDEX idx_municipio on estabelecimento (municipio)')
        op.execute('CREATE INDEX idx_situacao_cadastral on estabelecimento (situacao_cadastral)')

