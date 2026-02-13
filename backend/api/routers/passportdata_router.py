from fastapi import APIRouter, Depends
from db.sql.schemas.passportdata_schema import PassportDataResponse, PassportDataCreate, PassportDataUpdate
from services.passportdata_service import PassportDataService

router = APIRouter(prefix="/passportdata", tags=["PassportData"])

@router.post("/", response_model=PassportDataResponse, status_code=201)
async def create_passport_data(passport_data: PassportDataCreate, service: PassportDataService = Depends(PassportDataService)):
    return await service.create_passport_data(passport_data)

@router.get("/{passport_id}", response_model=PassportDataResponse)
async def get_passport_data(passport_id: int, service: PassportDataService = Depends(PassportDataService)):
    return await service.get_passport_data(passport_id)

@router.get("/user/{user_id}", response_model=PassportDataResponse)
async def get_passport_data_by_user(user_id: int, service: PassportDataService = Depends(PassportDataService)):
    return await service.get_passport_data_by_user(user_id)

@router.put("/{passport_id}", response_model=PassportDataResponse)
async def update_passport_data(passport_id: int, passport_data: PassportDataUpdate, service: PassportDataService = Depends(PassportDataService)):
    return await service.update_passport_data(passport_id, passport_data)

@router.delete("/{passport_id}")
async def delete_passport_data(passport_id: int, service: PassportDataService = Depends(PassportDataService)):
    await service.delete_passport_data(passport_id)
    return {"message": "Passport data deleted successfully"}

@router.delete("/user/{user_id}")
async def delete_passport_data_by_user(user_id: int, service: PassportDataService = Depends(PassportDataService)):
    await service.delete_passport_data_by_user(user_id)
    return {"message": "Passport data deleted successfully"}