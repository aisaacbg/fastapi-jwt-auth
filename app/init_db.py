from .database import engine
from .models import Base

def init_db():
    # Crear las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
