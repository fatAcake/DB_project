from fastapi import Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_postgres_db
from db.sql.schemas.blueprints_schemas import BlueprintInfo


async def get_blueprint_info_from_query(
    blueprint_id_sql: int = Query(..., gt=0),
    session: AsyncSession = Depends(get_postgres_db)
) -> BlueprintInfo:
    """Зависимость для получения информации о чертеже из Query параметра"""
    from db.sql.crud.blueprints_crud import get_blueprint
    
    blueprint = await get_blueprint(session, blueprint_id_sql)
    if not blueprint:
        raise HTTPException(404, "Blueprint not found")
    
    return BlueprintInfo(
        id=blueprint.id,
        name=blueprint.name,
        description=blueprint.description
    )

async def get_blueprint_info_from_path(
    blueprint_id_sql: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_postgres_db)
) -> BlueprintInfo:
    """Зависимость для получения информации о чертеже из Path параметра"""
    from db.sql.crud.blueprints_crud import get_blueprint
    
    blueprint = await get_blueprint(session, blueprint_id_sql)
    if not blueprint:
        raise HTTPException(404, "Blueprint not found")
    
    return BlueprintInfo(
        id=blueprint.id,
        name=blueprint.name,
        description=blueprint.description
    )