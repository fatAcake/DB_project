# Картинки для MongoDB-сида

Сид `seed_mongo.py` подставляет изображения **из файлов** по путям.

Положите в эту папку:

- **product_1.jpg** … **product_5.jpg** — изображения продуктов (id 1–5, см. `seed_data.py` PRODUCTS_DATA).
- **blueprint_1.jpg** … **blueprint_5.jpg** — изображения чертежей (id 1–5).

Поддерживаются форматы: `.jpg`, `.jpeg`, `.png`, `.webp`.

Если файла нет или путь не задан — в MongoDB попадёт минимальная PNG-заглушка (1×1 px), как раньше.

Пути задаются в `seed_mongo.py` константами `SEED_IMAGE_PATHS_PRODUCTS` и `SEED_IMAGE_PATHS_BLUEPRINTS`; по умолчанию используются файлы из этой папки.
