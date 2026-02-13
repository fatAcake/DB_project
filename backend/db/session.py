import json
import logging
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import config
from db.sql.models import Base as SQLBase

# === PostgreSQL ===
async_postgres_engine = create_async_engine(config.POSTGRES_URL, echo=config.ECHO)

AsyncSessionLocalPostgres = sessionmaker(
    bind=async_postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_postgres_db():
    """Инициализация базы данных PostgreSQL"""
    logger = logging.getLogger("uvicorn")
    
    async with async_postgres_engine.begin() as conn:
        def check_tables_sync(connection):
            inspector = inspect(connection)
            return set(inspector.get_table_names())
        
        existing_tables = await conn.run_sync(check_tables_sync)
        metadata_tables = set(SQLBase.metadata.tables.keys())
        missing_tables = metadata_tables - existing_tables
        
        if not missing_tables:
            logger.info(f"БД: все таблицы существуют ({len(existing_tables)}/{len(metadata_tables)})")
        else:
            logger.info(f"БД: создание {len(missing_tables)} таблиц")
            await conn.run_sync(SQLBase.metadata.create_all)
            logger.info("БД: таблицы созданы")


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

# === MongoDB ===
mongo_client = AsyncIOMotorClient(config.MONGO_URL)
mongo_db = mongo_client[config.MONGO_DB]

# Коллекции для хранения файлов напрямую в документах
products_images_collection = mongo_db["products_images"]
blueprints_collection = mongo_db["blueprints"]

async def init_mongo_db():
    try:
        await mongo_db.command("ping")
        print("MongoDB подключена")
        
        # Индексы для быстрого поиска по связям с SQL
        await products_images_collection.create_index([("product_id_sql", 1)])
        await blueprints_collection.create_index([("blueprint_id_sql", 1)])
        
        print("Индексы созданы")
    except Exception as e:
        print(f"Ошибка MongoDB: {e}")
        raise

async def close_mongo_connection():
    mongo_client.close()

async def init_db_on_start_up():
    await init_postgres_db()
    await init_mongo_db()