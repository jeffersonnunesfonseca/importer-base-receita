# Base baixada direto do site da receita federal
- https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj

```
CREATE SCHEMA `base_cnpj` ;
```
# Instalar dependências
```
pip install -r requirements.txt
``` 

# Config
- Seta string de conexão no alembic.ini e exportar como variavel de ambiente
```
alembic.ini:38 = sqlalchemy.url = mysql+pymysql://teste:teste@localhost/base_cnpj

export DATABASE_URL=mysql+pymysql://teste:teste@localhost/base_cnpj

```
- subindo tabelas com o alembic
```
alembic upgrade head
```

# TODO - processo de agrupamento dos arquivos baixados
- a fazer ...

# Importando arquivo
- executar o arquivo 'import_base.sh', irá disparar 3 processos de importaçãos, empresa, socios e estabelecimentos
```
sh import_base.sh
```