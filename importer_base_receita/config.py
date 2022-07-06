import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost/basecnpj")
