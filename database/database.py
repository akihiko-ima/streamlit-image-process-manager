import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
DB_PATH = os.getenv("DB_PATH")

# データベースのURL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# データベースエンジン
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLiteのスレッドチェックを無効化
)

# セッションローカルを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラスを作成
Base = declarative_base()


def create_tables():
    """テーブル作成"""
    Base.metadata.create_all(engine)


def get_db():
    """データベースセッションを取得する関数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
