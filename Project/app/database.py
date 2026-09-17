from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config import setting
connect_args = {"check_same_thread": False} if setting.database_url.startswith("sqlite") else {}
engine=create_engine(setting.database_url,connect_args=connect_args)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()