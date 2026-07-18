import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABSE_URL",
    "postgresql://postgres:password@localhost:5432/sales_db"
)

def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)

def test_connection():
    engine = get_engine()
    with engine.connect() as conn:
      result = conn.execute(text("SELECT version()"))
      print("👍 Connected:", result.scalar())

if __name__ == "__main__":
    test_connection()