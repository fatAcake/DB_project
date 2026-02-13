from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_postgres_db
from services.transactions_service import TransactionsService
from db.sql.schemas.transactions_schemas import TransactionCreate, TransactionUpdate, TransactionInfo

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/", response_model=TransactionInfo)
async def create_transaction(
    data: TransactionCreate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Создание новой транзакции"""
    service = TransactionsService(session)
    return await service.create(data)


@router.get("/{transaction_id}", response_model=TransactionInfo)
async def get_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение транзакции по ID"""
    service = TransactionsService(session)
    return await service.get_by_id(transaction_id)


@router.get("/", response_model=List[TransactionInfo])
async def get_transactions(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    session: AsyncSession = Depends(get_postgres_db)
):
    """Получение списка транзакций"""
    service = TransactionsService(session)
    return await service.get_all(skip, limit)


@router.put("/{transaction_id}", response_model=TransactionInfo)
async def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Обновление транзакции"""
    service = TransactionsService(session)
    return await service.update(transaction_id, data)


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_postgres_db)
):
    """Удаление транзакции"""
    service = TransactionsService(session)
    await service.delete(transaction_id)
    return {"message": "Transaction deleted successfully", "transaction_id": transaction_id, "status_code": 200}