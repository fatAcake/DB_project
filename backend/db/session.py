"""
Сессия и инициализация БД.
Защита от SQL-инъекций: все запросы к PostgreSQL выполняются через SQLAlchemy ORM
(select/where/insert/update/delete с привязкой параметров), без подстановки строк в SQL.
Единственное место с сырым SQL — создание базы при старте (идентификатор проверяется regex и экранируется).
"""
import json
import logging
import re
import asyncpg
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import config
from db.sql.models import Base as SQLBase

# === PostgreSQL ===


async def ensure_postgres_database_exists():
    """
    Проверяет существование базы данных PostgreSQL. Если базы нет — создаёт её.
    Подключается к служебной БД 'postgres', т.к. к несуществующей БД подключиться нельзя.
    """
    logger = logging.getLogger("uvicorn")
    # Имя БД: только буквы, цифры, подчёркивание (защита от SQL-инъекций в идентификатор)
    db_name = config.POSTGRES_DB
    if not re.match(r"^[a-zA-Z0-9_]+$", db_name):
        logger.warning("ensure_postgres_database_exists: небезопасное имя БД, пропуск создания")
        return
    # Экранирование кавычки в идентификаторе (на случай расширения правил имени)
    safe_ident = '"' + db_name.replace('"', '""') + '"'
    try:
        conn = await asyncpg.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database="postgres",
        )
        try:
            # Параметризованный запрос — данные не подставляются в SQL как текст
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_name
            )
            if exists is None:
                # Идентификатор уже проверен regex и экранирован
                await conn.execute(f"CREATE DATABASE {safe_ident}")
                logger.info("БД: база данных %s создана", db_name)
            else:
                logger.info("БД: база данных %s уже существует", db_name)
        finally:
            await conn.close()
    except Exception as e:
        logger.exception("Ошибка проверки/создания базы данных: %s", e)
        raise


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
    await ensure_postgres_database_exists()
    await init_postgres_db()
    from db.seed_data import seed_db
    await seed_db()
    await init_mongo_db()
    from db.seed_mongo import seed_mongo
    await seed_mongo()