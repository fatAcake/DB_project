"""
Сид тестовых данных для MongoDB.
Добавляет по одному документу-заглушке (минимальное изображение) для каждого продукта
и каждого чертежа из PostgreSQL (product_id_sql / blueprint_id_sql 1..5).
Вызывается после init_mongo_db(), только если документов ещё мало.
"""
import logging
from datetime import datetime
from bson import Binary

from db.session import products_images_collection, blueprints_collection

logger = logging.getLogger("uvicorn")

SEED_MIN_COUNT = 5

# Минимальный валидный PNG 1×1 пиксель (~68 байт) — заглушка для картинок
MINIMAL_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
    b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


async def _need_seed_products() -> bool:
    count = await products_images_collection.count_documents({})
    return count < SEED_MIN_COUNT


async def _need_seed_blueprints() -> bool:
    count = await blueprints_collection.count_documents({})
    return count < SEED_MIN_COUNT


async def seed_mongo() -> None:
    """Заполняет коллекции MongoDB тестовыми документами с заглушкой-картинкой."""
    try:
        added_products = 0
        if await _need_seed_products():
            for product_id_sql in range(1, SEED_MIN_COUNT + 1):
                await products_images_collection.insert_one(
                    {
                        "image": Binary(MINIMAL_PNG),
                        "filename": f"placeholder_product_{product_id_sql}.png",
                        "content_type": "image/png",
                        "product_id_sql": product_id_sql,
                        "created_at": datetime.utcnow(),
                    }
                )
                added_products += 1
            logger.info("MongoDB сид: добавлено %s изображений продуктов", added_products)

        added_blueprints = 0
        if await _need_seed_blueprints():
            for blueprint_id_sql in range(1, SEED_MIN_COUNT + 1):
                await blueprints_collection.insert_one(
                    {
                        "image": Binary(MINIMAL_PNG),
                        "filename": f"placeholder_blueprint_{blueprint_id_sql}.png",
                        "content_type": "image/png",
                        "blueprint_id_sql": blueprint_id_sql,
                        "created_at": datetime.utcnow(),
                    }
                )
                added_blueprints += 1
            logger.info("MongoDB сид: добавлено %s чертежей", added_blueprints)

        if added_products == 0 and added_blueprints == 0:
            logger.info("MongoDB сид: данные уже есть, пропуск")
    except Exception as e:
        logger.exception("MongoDB сид: ошибка заполнения: %s", e)
        raise
