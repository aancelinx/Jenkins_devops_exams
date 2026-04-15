# Mock db_manager sans base de données
from typing import List, Dict, Any

async def get_all_casts() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "name": "Tom Hanks", "role": "Lead"},
        {"id": 2, "name": "Scarlett Johansson", "role": "Lead"},
        {"id": 3, "name": "Robert Downey Jr.", "role": "Supporting"}
    ]

async def get_cast(cast_id: int) -> Dict[str, Any]:
    return {"id": cast_id, "name": f"Actor {cast_id}", "role": "Actor"}

async def create_cast(cast: Dict[str, Any]) -> int:
    return 1

async def delete_cast(cast_id: int) -> int:
    return 1
