from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient 
from core.config import config
from db.sql.models import Base as SQLBase

# === PostgreSQL (SQL) ===
async_postgres_engine = create_async_engine(config.POSTGRES_URL, echo=config.ECHO) 

AsyncSessionLocalPostgres = sessionmaker(
    bind=async_postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_postgres_db():
    async with async_postgres_engine.begin() as conn:
        await conn.run_sync(SQLBase.metadata.create_all)

async def drop_postgres_db():
    async with async_postgres_engine.begin() as conn:
        await conn.run_sync(SQLBase.metadata.drop_all)

async def get_postgres_db():
    async with AsyncSessionLocalPostgres() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# === MongoDB (NoSQL) ===
mongo_client = AsyncIOMotorClient(config.MONGO_URL)
mongo_db = mongo_client[config.MONGO_DB]  

async def get_mongo_db():
    yield mongo_db

async def init_mongo_db():
    try:
        await mongo_db.command("ping")
        print("MongoDB подключена")
    except Exception as e:
        print(f"Ошибка подключения к MongoDB: {e}")
        raise

async def close_mongo_connection():
    mongo_client.close()

# === Инициализация при старте ===
async def init_db_on_start_up():
    await init_postgres_db()
    await init_mongo_db() 