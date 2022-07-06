from sqlalchemy import create_engine, text
from importer_base_receita import config

db_engine = create_engine(config.DATABASE_URL,
    pool_size=10,
    max_overflow=10,
    pool_recycle=60 * 60 * 1,
    pool_timeout=30,
    isolation_level='READ COMMITTED'
)
