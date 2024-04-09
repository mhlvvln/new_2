import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# from models import User


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# выгрузка и создание таблиц
async def init_models():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
