from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_postgres_db
from services.feedback_service import FeedbackService
from db.sql.schemas.feedback_schemas import FeedbackCreate, FeedbackUpdate, FeedbackInfo

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.post("/", response_model=FeedbackInfo)
async def create_feedback(
    data: FeedbackCreate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Создание новой обратной связи"""
    service = FeedbackService(session)
    return await service.create(data)


@router.get("/{feedback_id}", response_model=FeedbackInfo)
async def get_feedback(
    feedback_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение обратной связи по ID"""
    service = FeedbackService(session)
    return await service.get_by_id(feedback_id)


@router.get("/", response_model=List[FeedbackInfo])
async def get_feedbacks(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение списка обратной связи"""
    service = FeedbackService(session)
    return await service.get_all(skip, limit)


@router.put("/{feedback_id}", response_model=FeedbackInfo)
async def update_feedback(
    feedback_id: int,
    data: FeedbackUpdate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Обновление обратной связи"""
    service = FeedbackService(session)
    return await service.update(feedback_id, data)


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление обратной связи"""
    service = FeedbackService(session)
    await service.delete(feedback_id)
    return {"message": "Feedback deleted successfully", "feedback_id": feedback_id, "status_code": 200}