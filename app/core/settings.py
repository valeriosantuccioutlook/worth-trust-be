from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from ..config import DB_URI

# Create session
engine = create_engine(url=DB_URI, echo=True)
SessionLocal: Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
