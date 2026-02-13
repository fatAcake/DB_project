from datetime import datetime
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from db.sql.models import Feedback
from db.sql.schemas.feedback_schemas import FeedbackCreate, FeedbackUpdate


async def create_feedback(session: AsyncSession, data: FeedbackCreate) -> Feedback | None:
    """Создание обратной связи"""
    try:
        feedback = Feedback(**data.model_dump())
        session.add(feedback)
        await session.commit()
        await session.refresh(feedback)
        return feedback
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка создания обратной связи",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_feedback(session: AsyncSession, feedback_id: int) -> Feedback | None:
    """Получение обратной связи по ID"""
    try:
        result = await session.execute(
            select(Feedback).where(Feedback.id == feedback_id)
        )
        feedback = result.scalar_one_or_none()
        return feedback
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения обратной связи",
            "feedback_id": feedback_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def get_feedbacks(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Feedback] | None:
    """Получение списка обратной связи"""
    try:
        result = await session.execute(
            select(Feedback)
            .offset(skip)
            .limit(limit)
        )
        feedbacks = result.scalars().all()
        return list(feedbacks)
    except Exception as e:
        logging.error(json.dumps({
            "message": "Ошибка получения списка обратной связи",
            "skip": skip,
            "limit": limit,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def update_feedback(session: AsyncSession, feedback_id: int, data: FeedbackUpdate) -> Feedback | None:
    """Обновление обратной связи"""
    try:
        feedback = await get_feedback(session, feedback_id)
        if not feedback:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(feedback, field, value)
        
        await session.commit()
        await session.refresh(feedback)
        return feedback
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка обновления обратной связи",
            "feedback_id": feedback_id,
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return None


async def delete_feedback(session: AsyncSession, feedback_id: int) -> bool:
    """Удаление обратной связи"""
    try:
        result = await session.execute(
            delete(Feedback).where(Feedback.id == feedback_id)
        )
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        logging.error(json.dumps({
            "message": "Ошибка удаления обратной связи",
            "feedback_id": feedback_id,
            "error": str(e),
            "time": datetime.now().isoformat(),
        }))
        return False