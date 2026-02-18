from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.sql.crud.transactions_crud import (
    create_transaction, get_transaction, get_transactions,
    update_transaction, delete_transaction
)
from db.sql.schemas.transactions_schemas import TransactionCreate, TransactionUpdate, TransactionInfo


class TransactionsService:
    """Сервис для работы с транзакциями"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TransactionCreate) -> TransactionInfo:
        """Создание транзакции"""
        transaction = await create_transaction(self.session, data)
        if not transaction:
            raise HTTPException(400, "Failed to create transaction")
        
        return TransactionInfo(
            id=transaction.id,
            sum=transaction.sum,
            card_data=transaction.card_data,
            user_id=transaction.user_id,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )

    async def get_by_id(self, transaction_id: int) -> TransactionInfo:
        """Получение транзакции по ID"""
        transaction = await get_transaction(self.session, transaction_id)
        if not transaction:
            raise HTTPException(404, "Transaction not found")
        
        return TransactionInfo(
            id=transaction.id,
            sum=transaction.sum,
            card_data=transaction.card_data,
            user_id=transaction.user_id,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TransactionInfo]:
        """Получение списка транзакций"""
        transactions = await get_transactions(self.session, skip, limit)
        if not transactions:
            raise HTTPException(404, "No transactions found")
        
        return [
            TransactionInfo(
                id=transaction.id,
                sum=transaction.sum,
                card_data=transaction.card_data,
                user_id=transaction.user_id,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at
            )
            for transaction in transactions
        ]

    async def update(self, transaction_id: int, data: TransactionUpdate) -> TransactionInfo:
        """Обновление транзакции"""
        transaction = await update_transaction(self.session, transaction_id, data)
        if not transaction:
            raise HTTPException(404, "Transaction not found")
        
        return TransactionInfo(
            id=transaction.id,
            sum=transaction.sum,
            card_data=transaction.card_data,
            user_id=transaction.user_id,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )

    async def delete(self, transaction_id: int) -> bool:
        """Удаление транзакции"""
        success = await delete_transaction(self.session, transaction_id)
        if not success:
            raise HTTPException(404, "Transaction not found")
        return True