from datetime import datetime
from fastapi import APIRouter, File, UploadFile, Query, HTTPException, Depends
from typing import List
from fastapi.responses import Response
from urllib.parse import quote
from db.nosql.models import ProductImageResponse
from services.products_images_service import ProductsImagesService
from dependencies import get_products_images_service


router = APIRouter(prefix="/files_products", tags=["FilesProducts"])


@router.post("/", response_model=ProductImageResponse)
async def upload_product_image(
    file: UploadFile = File(...),
    product_id_sql: int = Query(..., gt=0),
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Загрузка изображения продукта"""
    image = await service.upload_image(
        file=file,
        product_id_sql=product_id_sql
    )
    # Возвращаем ответ без бинарных данных
    return ProductImageResponse(
        id=image.id,
        product_id_sql=image.product_id_sql,
        filename=image.filename,
        content_type=image.content_type,
        created_at=image.created_at,
        image_size=len(image.image) if image.image else 0
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
        image_size=len(image.image)
    )


@router.get("/", response_model=List[ProductImageResponse])
async def get_all_products_images(
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Получение всех изображений продуктов"""
    images = await service.get_all()
    
    if not images:
        raise HTTPException(404, "No images found")
    
    return [
        ProductImageResponse(
            id=doc["_id"],
            product_id_sql=doc["product_id_sql"],
            filename=doc["filename"],
            content_type=doc.get("content_type", "application/octet-stream"),
            created_at=doc.get("created_at", datetime.utcnow()),
            image_size=len(doc.get("image", b""))
        )
        for doc in images
    ]


@router.get("/{product_id_sql}/images", response_model=List[ProductImageResponse])
async def get_product_images(
    product_id_sql: int,
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Получение всех изображений продукта"""
    images = await service.get_product_images(product_id_sql)
    
    return [
        ProductImageResponse(
            id=img.id,
            product_id_sql=img.product_id_sql,
            filename=img.filename,
            content_type=img.content_type,
            created_at=img.created_at,
            image_size=len(img.image) if img.image else 0
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
    
    return {"message": "Image deleted successfully"}


@router.delete("/{product_id_sql}/images")
async def delete_all_product_images(
    product_id_sql: int,
    service: ProductsImagesService = Depends(get_products_images_service)
):
    """Удаление всех изображений продукта"""
    count = await service.delete_product_images(product_id_sql)
    return {"deleted_count": count}