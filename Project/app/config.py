from dotenv import load_dotenv

load_dotenv()
import os

class Settings:
    database_url: str = os.getenv("Database_url")
    algorithm: str = os.getenv("algorthim")
    secret_key: str = os.getenv("my_secret_key")

setting=Settings()