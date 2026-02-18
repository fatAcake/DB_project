from datetime import datetime, timezone
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from db.sql.models import Transactions
from db.sql.schemas.transactions_schemas import TransactionCreate, TransactionUpdate


logger = logging.getLogger(__name__)


async def create_transaction(session: AsyncSession, data: TransactionCreate) -> Transactions | None:
    """Создание транзакции"""
    try:
        transaction = Transactions(
            **data.model_dump(),
            created_at=datetime.now(timezone.utc)
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка создания транзакции",
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now(timezone.utc).isoformat(),
        }))
        return None


async def get_transaction(session: AsyncSession, transaction_id: int) -> Transactions | None:
    """Получение транзакции по ID"""
    try:
        result = await session.execute(
            select(Transactions).where(Transactions.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        return transaction
    except Exception as e:
        logger.error(json.dumps({
            "message": "Ошибка получения транзакции",
            "transaction_id": transaction_id,
            "error": str(e),
            "time": datetime.now(timezone.utc).isoformat(),
        }))
        return None


async def get_transactions(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Transactions] | None:
    """Получение списка транзакций"""
    try:
        result = await session.execute(
            select(Transactions)
            .offset(skip)
            .limit(limit)
            .order_by(Transactions.created_at.desc())
        )
        transactions = result.scalars().all()
        return list(transactions)
    except Exception as e:
        logger.error(json.dumps({
            "message": "Ошибка получения списка транзакций",
            "skip": skip,
            "limit": limit,
            "error": str(e),
            "time": datetime.now(timezone.utc).isoformat(),
        }))
        return None


async def update_transaction(session: AsyncSession, transaction_id: int, data: TransactionUpdate) -> Transactions | None:
    """Обновление транзакции"""
    try:
        transaction = await get_transaction(session, transaction_id)
        if not transaction:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaction, field, value)
        
        transaction.updated_at = datetime.now(timezone.utc)
        
        await session.commit()
        await session.refresh(transaction)
        return transaction
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка обновления транзакции",
            "transaction_id": transaction_id,
            "data": data.model_dump(),
            "error": str(e),
            "time": datetime.now(timezone.utc).isoformat(),
        }))
        return None


async def delete_transaction(session: AsyncSession, transaction_id: int) -> bool:
    """Удаление транзакции"""
    try:
        result = await session.execute(
            delete(Transactions).where(Transactions.id == transaction_id)
        )
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        logger.error(json.dumps({
            "message": "Ошибка удаления транзакции",
            "transaction_id": transaction_id,
            "error": str(e),
            "time": datetime.now(timezone.utc).isoformat(),
        }))
        return False