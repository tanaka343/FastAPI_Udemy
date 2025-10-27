from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

SQLALCHEMY_URL = "postgresql://fastapiuser:fastapipass@localhost:5432/fleamarket"

engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

def get_data():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()