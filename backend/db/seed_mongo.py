"""
Сид тестовых данных для MongoDB.
Добавляет по одному документу для каждого продукта и чертежа из PostgreSQL
(product_id_sql / blueprint_id_sql 1..5). Картинки берутся из файлов по путям;
если файла нет — используется минимальная PNG-заглушка.
Вызывается после init_mongo_db(), только если документов ещё мало.
"""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from bson import Binary

from db.session import products_images_collection, blueprints_collection

logger = logging.getLogger("uvicorn")

SEED_MIN_COUNT = 5

# Каталог с картинками для сида (относительно этого файла). Положите сюда:
# product_1.jpg ... product_5.jpg, blueprint_1.jpg ... blueprint_5.jpg (или .png)
SEED_IMAGES_DIR = Path(__file__).resolve().parent / "seed_images"

# Пути к картинкам продуктов (id 1..5). Если None или файл не найден — используется заглушка.
SEED_IMAGE_PATHS_PRODUCTS = [
    SEED_IMAGES_DIR / "product_1.jpg",
    SEED_IMAGES_DIR / "product_2.jpg",
    SEED_IMAGES_DIR / "product_3.jpg",
    SEED_IMAGES_DIR / "product_4.jpg",
    SEED_IMAGES_DIR / "product_5.jpg",
]

# Пути к картинкам чертежей (id 1..5).
SEED_IMAGE_PATHS_BLUEPRINTS = [
    SEED_IMAGES_DIR / "blueprint_1.jpg",
    SEED_IMAGES_DIR / "blueprint_2.jpg",
    SEED_IMAGES_DIR / "blueprint_3.jpg",
    SEED_IMAGES_DIR / "blueprint_4.jpg",
    SEED_IMAGES_DIR / "blueprint_5.jpg",
]

# Минимальный валидный PNG 1×1 пиксель — заглушка, если файл по пути не найден
MINIMAL_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
    b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _load_image_from_path(path: Optional[Path]) -> tuple[bytes, str, str]:
    """
    Читает картинку из файла. Возвращает (bytes, content_type, filename).
    Если путь None или файл не найден — возвращает MINIMAL_PNG и content_type image/png.
    """
    if path is None or not path.is_file():
        return MINIMAL_PNG, "image/png", "placeholder.png"
    try:
        data = path.read_bytes()
    except OSError as e:
        logger.warning("Сид MongoDB: не удалось прочитать %s: %s", path, e)
        return MINIMAL_PNG, "image/png", "placeholder.png"
    suffix = path.suffix.lower()
    content_type = "image/png"
    if suffix in (".jpg", ".jpeg"):
        content_type = "image/jpeg"
    elif suffix == ".webp":
        content_type = "image/webp"
    return data, content_type, path.name


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
                path = SEED_IMAGE_PATHS_PRODUCTS[product_id_sql - 1] if product_id_sql <= len(SEED_IMAGE_PATHS_PRODUCTS) else None
                image_bytes, content_type, filename = _load_image_from_path(path)
                await products_images_collection.insert_one(
                    {
                        "image": Binary(image_bytes),
                        "filename": filename,
                        "content_type": content_type,
                        "product_id_sql": product_id_sql,
                        "created_at": datetime.utcnow(),
                    }
                )
                added_products += 1
            logger.info("MongoDB сид: добавлено %s изображений продуктов", added_products)

        added_blueprints = 0
        if await _need_seed_blueprints():
            for blueprint_id_sql in range(1, SEED_MIN_COUNT + 1):
                path = SEED_IMAGE_PATHS_BLUEPRINTS[blueprint_id_sql - 1] if blueprint_id_sql <= len(SEED_IMAGE_PATHS_BLUEPRINTS) else None
                image_bytes, content_type, filename = _load_image_from_path(path)
                await blueprints_collection.insert_one(
                    {
                        "image": Binary(image_bytes),
                        "filename": filename,
                        "content_type": content_type,
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
