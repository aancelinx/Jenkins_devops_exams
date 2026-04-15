from fastapi import APIRouter, HTTPException
from typing import List
from app.api import db_manager

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_casts():
    return await db_manager.get_all_casts()

@router.get("/{cast_id}", response_model=dict)
async def get_cast(cast_id: int):
    cast = await db_manager.get_cast(cast_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast

@router.post("/", response_model=int)
async def create_cast(cast: dict):
    return await db_manager.create_cast(cast)

@router.delete("/{cast_id}")
async def delete_cast(cast_id: int):
    await db_manager.delete_cast(cast_id)
    return {"message": "Cast deleted"}
