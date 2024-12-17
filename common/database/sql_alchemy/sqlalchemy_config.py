from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# Carregando variáveis de ambiente do .env
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` para ver as queries no console
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter uma sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
