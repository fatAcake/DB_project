from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.sql.crud.feedback_crud import (
    create_feedback, get_feedback, get_feedbacks,
    update_feedback, delete_feedback
)
from db.sql.schemas.feedback_schemas import FeedbackCreate, FeedbackUpdate, FeedbackInfo


class FeedbackService:
    """Сервис для работы с обратной связью"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: FeedbackCreate) -> FeedbackInfo:
        """Создание обратной связи"""
        feedback = await create_feedback(self.session, data)
        if not feedback:
            raise HTTPException(400, "Failed to create feedback")
        
        return FeedbackInfo(
            id=feedback.id,
            message=feedback.message,
            user_id=feedback.user_id
        )

    async def get_by_id(self, feedback_id: int) -> FeedbackInfo:
        """Получение обратной связи по ID"""
        feedback = await get_feedback(self.session, feedback_id)
        if not feedback:
            raise HTTPException(404, "Feedback not found")
        
        return FeedbackInfo(
            id=feedback.id,
            message=feedback.message,
            user_id=feedback.user_id
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[FeedbackInfo]:
        """Получение списка обратной связи"""
        feedbacks = await get_feedbacks(self.session, skip, limit)
        if not feedbacks:
            raise HTTPException(404, "No feedback found")
        
        return [
            FeedbackInfo(
                id=feedback.id,
                message=feedback.message,
                user_id=feedback.user_id
            )
            for feedback in feedbacks
        ]

    async def update(self, feedback_id: int, data: FeedbackUpdate) -> FeedbackInfo:
        """Обновление обратной связи"""
        feedback = await update_feedback(self.session, feedback_id, data)
        if not feedback:
            raise HTTPException(404, "Feedback not found")
        
        return FeedbackInfo(
            id=feedback.id,
            message=feedback.message,
            user_id=feedback.user_id
        )

    async def delete(self, feedback_id: int) -> bool:
        """Удаление обратной связи"""
        success = await delete_feedback(self.session, feedback_id)
        if not success:
            raise HTTPException(404, "Feedback not found")
        return True