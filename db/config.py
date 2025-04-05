import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL
from pathlib import Path

# Шлях до .env у корені проєкту
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"

load_dotenv(dotenv_path=dotenv_path)

required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

def get_database_url():
    return str(
        URL.create(
            drivername="postgresql",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
    )
