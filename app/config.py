import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    # Configuración de JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Base de datos principal para los endpoints
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Base de datos de pruebas separada
    TEST_SQLALCHEMY_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL")

settings = Settings()
