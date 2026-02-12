from db.session import blueprints_collection
from db.session import products_images_collection
from db.nosql.crud.blueprint_images import BlueprintsCRUD
from db.nosql.crud.products_images import ProductsImagesCRUD
from services.blueprint_images_service import BlueprintsService
from services.products_images_service import ProductsImagesService

async def get_blueprints_service() -> BlueprintsService:
    """Фабрика для создания сервиса чертежей"""
    crud = BlueprintsCRUD(blueprints_collection)
    return BlueprintsService(crud)

async def get_products_images_service() -> ProductsImagesService:
    """Фабрика для создания сервиса изображений продуктов"""
    crud = ProductsImagesCRUD(products_images_collection)
    return ProductsImagesService(crud)