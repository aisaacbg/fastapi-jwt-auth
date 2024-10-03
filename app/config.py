import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Main database for endpoints
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Separate database for tests
    TEST_SQLALCHEMY_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL")

settings = Settings()
