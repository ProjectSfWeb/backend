import os
from dotenv import load_dotenv


load_dotenv()


class settings:
    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    LOG_LEVEL = os.getenv("LOG_LEVEL")
