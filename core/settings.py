import os
from dotenv import load_dotenv

# load_dotenv("core/.env")

class Settings:
    PROJECT_NAME: str = "GeoSAT"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_TEST_URL = os.getenv('DATABASE_TEST_URL')
    LOCAL_PATH = os.getenv('LOCAL_PATH')
    REDIS_HOST = os.getenv('REDIS_HOST','localhost')


settings = Settings()


