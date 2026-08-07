import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Try Streamlit secrets first, then fall back to environment variables
try:
    import streamlit as st
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)

def test_connection():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("✅ Connected:", result.scalar())

if __name__ == "__main__":
    test_connection()