from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


SQLALCHEMY_URL = "postgresql://fastapiuser:fastapipass@0.0.0.0:5432/fleamarket"
engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()