# Mock db_manager sans base de données
from typing import List, Dict, Any

async def get_all_movies() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "title": "Inception", "year": 2010, "rating": 8.8},
        {"id": 2, "title": "The Matrix", "year": 1999, "rating": 8.7},
        {"id": 3, "title": "Interstellar", "year": 2014, "rating": 8.6}
    ]

async def get_movie(movie_id: int) -> Dict[str, Any]:
    return {"id": movie_id, "title": f"Movie {movie_id}", "year": 2024, "rating": 9.0}

async def create_movie(movie: Dict[str, Any]) -> int:
    return 1

async def delete_movie(movie_id: int) -> int:
    return 1
