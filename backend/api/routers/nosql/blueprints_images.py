from fastapi import APIRouter, File, UploadFile, Query, HTTPException, Depends, Path
from typing import List, Optional
from fastapi.responses import Response
from urllib.parse import quote
from api.dependencies_methods.blueprints import get_blueprint_info_from_path, get_blueprint_info_from_query
from db.session import get_postgres_db
from db.sql.schemas.blueprints_schemas import BlueprintInfo  
from db.nosql.models import BlueprintResponse
from sqlalchemy.ext.asyncio import AsyncSession
from services.nosql.blueprint_images_service import BlueprintsService
from dependencies import get_blueprints_service

router = APIRouter(prefix="/files_blueprints", tags=["FilesBlueprints"])

@router.post("/", response_model=BlueprintResponse)
async def upload_blueprint(
    file: UploadFile = File(...),
    blueprint_id_sql: int = Query(..., gt=0),
    blueprint_info: BlueprintInfo = Depends(get_blueprint_info_from_query),
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Загрузка чертежа"""
    blueprint = await service.upload_blueprint(file, blueprint_id_sql)
    
    return BlueprintResponse(
        id=blueprint.id,
        blueprint_id_sql=blueprint.blueprint_id_sql,
        filename=blueprint.filename,
        content_type=blueprint.content_type,
        created_at=blueprint.created_at,
        image_size=len(blueprint.image) if blueprint.image else 0,
        name=blueprint_info.name,
        description=blueprint_info.description
    )


@router.get("/{blueprint_id}")
async def download_blueprint(
    blueprint_id: str,
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Скачивание чертежа"""
    blueprint = await service.get_blueprint(blueprint_id)
    safe_filename = quote(blueprint.filename, encoding='utf-8')

    return Response(
        content=blueprint.image,
        media_type=blueprint.content_type,
        headers={"Content-Disposition": f'inline; filename="{safe_filename}"'}
    )


@router.get("/{blueprint_id}/info", response_model=BlueprintResponse)
async def get_blueprint_info(
    blueprint_id: str,
    blueprint_id_sql: int = Query(..., gt=0),
    blueprint_info: BlueprintInfo = Depends(get_blueprint_info_from_query),
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Получение информации об изображении без скачивания"""
    bp = await service.get_blueprint(blueprint_id)
    
    return BlueprintResponse(
        id=bp.id,
        blueprint_id_sql=bp.blueprint_id_sql,
        filename=bp.filename,
        content_type=bp.content_type,
        created_at=bp.created_at,
        image_size=len(bp.image) if bp.image else 0,
        name=blueprint_info.name,
        description=blueprint_info.description
    )


@router.get("/", response_model=List[BlueprintResponse])
async def get_all_blueprints_images(
    session: AsyncSession = Depends(get_postgres_db),
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Получение всех чертежей со всей информацией"""
    from db.sql.crud.blueprints_crud import get_blueprint
    
    blueprints = await service.get_blueprints()
    
    if not blueprints:
        raise HTTPException(404, "No blueprints found")
    
    # Получаем информацию о каждом чертеже из базы данных
    result = []
    for doc in blueprints:
        blueprint_id_sql = doc.get("blueprint_id_sql")
        
        # Получаем информацию о чертеже
        blueprint_info = await get_blueprint(session, blueprint_id_sql)
        
        result.append(
            BlueprintResponse(
                id=doc["_id"],
                blueprint_id_sql=blueprint_id_sql,
                filename=doc["filename"],
                content_type=doc.get("content_type", "application/octet-stream"),
                created_at=doc.get("created_at"),
                image_size=len(doc.get("image", b"")),
                name=blueprint_info.name if blueprint_info else None,
                description=blueprint_info.description if blueprint_info else None
            )
        )
    
    return result


@router.get("/sql/{blueprint_id_sql}", response_model=List[BlueprintResponse])
async def get_blueprint_versions(
    blueprint_id_sql: int = Path(..., gt=0),
    blueprint_info: BlueprintInfo = Depends(get_blueprint_info_from_path),
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Получение всех чертежей для записи"""
    blueprints = await service.get_blueprint_versions(blueprint_id_sql)
    
    if not blueprints:
        raise HTTPException(404, "No blueprints found for this blueprint")
    
    return [
        BlueprintResponse(
            id=bp.id,
            blueprint_id_sql=bp.blueprint_id_sql,
            filename=bp.filename,
            content_type=bp.content_type,
            created_at=bp.created_at,
            image_size=len(bp.image) if bp.image else 0,
            name=blueprint_info.name,
            description=blueprint_info.description
        )
        for bp in blueprints
    ]


@router.delete("/{blueprint_id}")
async def delete_blueprint(
    blueprint_id: str,
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Удаление чертежа"""
    success = await service.delete_blueprint(blueprint_id)
    if not success:
        raise HTTPException(404, "Blueprint not found")

    return {"message": "Blueprint deleted successfully", "status_code": 200}


@router.delete("/sql/{blueprint_id_sql}")
async def delete_all_blueprints(
    blueprint_id_sql: int = Path(..., gt=0),
    service: BlueprintsService = Depends(get_blueprints_service)
):
    """Удаление всех чертежей для записи"""
    count = await service.delete_blueprint_versions(blueprint_id_sql)
    return {"deleted_count": count, "status_code": 200}