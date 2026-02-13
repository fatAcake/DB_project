from fastapi import APIRouter, Depends, Query
from typing import List
from db.sql.schemas.logs_schema import LogResponse, LogCreate, LogUpdate
from services.logs_service import LogsService

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=LogResponse, status_code=201)
async def create_log(log_data: LogCreate, service: LogsService = Depends(LogsService)):
    return await service.create_log(log_data)

@router.get("/{log_id}", response_model=LogResponse)
async def get_log(log_id: int, service: LogsService = Depends(LogsService)):
    return await service.get_log(log_id)

@router.get("/user/{user_id}", response_model=List[LogResponse])
async def get_logs_by_user(user_id: int, service: LogsService = Depends(LogsService)):
    return await service.get_logs_by_user(user_id)

@router.get("/", response_model=List[LogResponse])
async def get_all_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: LogsService = Depends(LogsService)
):
    return await service.get_all_logs(skip, limit)

@router.put("/{log_id}", response_model=LogResponse)
async def update_log(log_id: int, log_data: LogUpdate, service: LogsService = Depends(LogsService)):
    return await service.update_log(log_id, log_data)

@router.delete("/{log_id}")
async def delete_log(log_id: int, service: LogsService = Depends(LogsService)):
    await service.delete_log(log_id)
    return {"message": "Log deleted successfully"}

@router.delete("/user/{user_id}")
async def delete_logs_by_user(user_id: int, service: LogsService = Depends(LogsService)):
    count = await service.delete_logs_by_user(user_id)
    return {"deleted_count": count}