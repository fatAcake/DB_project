from datetime import datetime
from fastapi import APIRouter, File, UploadFile, Query, HTTPException, Depends, Path
from typing import List
from fastapi.responses import Response
from urllib.parse import quote
from db.session import get_postgres_db
from db.sql.schemas.products_schemas import ProductInfo
from db.nosql.models import ProductImageResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.nosql.products_images_service import ProductsImagesService
from dependencies import get_products_images_service


router = APIRouter(prefix="/files_products", tags=["FilesProducts"])

async def get_product_info_from_query(
    product_id_sql: int = Query(..., gt=0),
    session: AsyncSession = Depends(get_postgres_db)
) -> ProductInfo:
    """Зависимость для получения информации о продукте из Query параметра"""
    from db.sql.crud.products_crud import get_product
    
    product = await get_product(session, product_id_sql)
    if not product:
        raise HTTPException(404, "Product not found")
    
    return ProductInfo(
        id=product.id,
        description=product.description,
        price=product.price
    )


async def get_product_info_from_path(
    product_id_sql: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_postgres_db)
) -> ProductInfo:
    """Зависимость для получения информации о продукте из Path параметра"""
    from db.sql.crud.products_crud import get_product
    
    product = await get_product(session, product_id_sql)
    if not product:
        raise HTTPException(404, "Product not found")
    
    return ProductInfo(
        id=product.id,
        description=product.description,
        price=product.price
    )


@router.post("/", response_model=ProductImageResponse)
async def upload_product_image(
    file: UploadFile = File(...),
    product_id_sql: int = Query(..., gt=0),
    product_info: ProductInfo = Depends(get_product_info_from_query),
    service: ProductsImagesService = Depends(get_products_images_service),
):
    """Загрузка изображения продукта"""
    image = await service.upload_image(
        file=file,
        product_id_sql=product_id_sql
    )
    
    return ProductImageResponse(
        id=image.id,
        product_id_sql=image.product_id_sql,
        filename=image.filename,
        content_type=image.content_type,
        created_at=image.created_at,
        image_size=len(image.image) if image.image else 0,
        price=product_info.price,
        description=product_info.description
    )


@router.get("/{image_id}")
async def download_product_image(
    image_id: str,
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Скачивание изображения продукта (только картинка)"""
    image = await service.get_image(image_id)
    
    safe_filename = quote(image.filename, encoding='utf-8')
    return Response(
        content=image.image,
        media_type=image.content_type,
        headers={"Content-Disposition": f'inline; filename="{safe_filename}"'}
    )


@router.get("/{image_id}/info", response_model=ProductImageResponse)
async def get_image_info(
    image_id: str,
    product_id_sql: int = Query(..., gt=0),
    product_info: ProductInfo = Depends(get_product_info_from_query),
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Получение информации об изображении без скачивания"""
    image = await service.get_image(image_id)
    
    return ProductImageResponse(
        id=image.id,
        product_id_sql=image.product_id_sql,
        filename=image.filename,
        content_type=image.content_type,
        created_at=image.created_at,
        image_size=len(image.image),
        price=product_info.price,
        description=product_info.description
    )


@router.get("/", response_model=List[ProductImageResponse])
async def get_all_products_images(
    product_id_sql: int = Query(..., gt=0),
    product_info: ProductInfo = Depends(get_product_info_from_query),
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Получение всех изображений продуктов для конкретного продукта"""
    images = await service.get_all()
    
    if not images:
        raise HTTPException(404, "No images found")
    
    # Фильтруем изображения по product_id_sql
    filtered_images = [doc for doc in images if doc.get("product_id_sql") == product_id_sql]
    
    if not filtered_images:
        raise HTTPException(404, f"No images found for product {product_id_sql}")
    
    return [
        ProductImageResponse(
            id=doc["_id"],
            product_id_sql=doc["product_id_sql"],
            filename=doc["filename"],
            content_type=doc.get("content_type", "application/octet-stream"),
            created_at=doc.get("created_at", datetime.utcnow()),
            image_size=len(doc.get("image", b"")),
            price=product_info.price,
            description=product_info.description
        )
        for doc in filtered_images
    ]


@router.get("/{product_id_sql}/images", response_model=List[ProductImageResponse])
async def get_product_images(
    product_id_sql: int = Path(..., gt=0),
    product_info: ProductInfo = Depends(get_product_info_from_path),
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Получение всех изображений продукта"""
    images = await service.get_product_images(product_id_sql)
    
    if not images:
        raise HTTPException(404, "No images found for this product")
    
    return [
        ProductImageResponse(
            id=img.id,
            product_id_sql=img.product_id_sql,
            filename=img.filename,
            content_type=img.content_type,
            created_at=img.created_at,
            image_size=len(img.image) if img.image else 0,
            price=product_info.price,
            description=product_info.description
        )
        for img in images
    ]


@router.delete("/{image_id}")
async def delete_product_image(
    image_id: str,
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Удаление изображения продукта"""
    success = await service.delete_image(image_id)
    
    if not success:
        raise HTTPException(404, "Image not found")
    
    return {"message": "Image deleted successfully", "status_code": 200}


@router.delete("/{product_id_sql}/images")
async def delete_all_product_images(
    product_id_sql: int = Path(..., gt=0),
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Удаление всех изображений продукта"""
    count = await service.delete_product_images(product_id_sql)
    return {"deleted_count": count, "status_code": 200}