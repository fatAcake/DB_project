from db.session import blueprints_collection
from db.nosql.crud.blueprint_images import BlueprintsCRUD
from db.nosql.crud.products_images import ProductsImagesCRUD
from services.blueprint_images_service import BlueprintsService
from services.products_images_service import ProductsImagesService

def get_blueprints_service() -> BlueprintsService:
    """Фабрика для создания сервиса чертежей"""
    crud = BlueprintsCRUD(blueprints_collection)
    return BlueprintsService(crud)

def get_products_images_service() -> ProductsImagesService:
    """Фабрика для создания сервиса изображений продуктов"""
    crud = ProductsImagesCRUD(blueprints_collection)
    return ProductsImagesService(crud)