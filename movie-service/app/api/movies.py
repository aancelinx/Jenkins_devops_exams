from fastapi import APIRouter, HTTPException
from typing import List
from app.api import db_manager

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_movies():
    return await db_manager.get_all_movies()

@router.get("/{movie_id}", response_model=dict)
async def get_movie(movie_id: int):
    movie = await db_manager.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=int)
async def create_movie(movie: dict):
    return await db_manager.create_movie(movie)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: int):
    await db_manager.delete_movie(movie_id)
    return {"message": "Movie deleted"}
