from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://turifydb_user:1FcJXmGEiwBOD73CqUVkJpbAM4Tf85ic@dpg-d19glhbe5dus738vpld0-a.oregon-postgres.render.com/turifydb"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()