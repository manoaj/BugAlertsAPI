from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

import Cred

SQLALCHEMY_DATABASE_URL = f"postgresql://{Cred.DB_USER}:{Cred.DB_PASSWORD}@{Cred.DB_HOST}:{Cred.DB_PORT}/{Cred.DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

if not database_exists(engine.url):
    create_database(engine.url)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()