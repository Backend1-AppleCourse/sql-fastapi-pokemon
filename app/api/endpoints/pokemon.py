# pokemon.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...db.database import PokemonDB, get_db_connection
from ...crud.pokemon_crud import get_pokemons_by_type
from ...schemas.pokemon import Pokemon

router = APIRouter()

@router.get("/by-type/{type_name}", response_model=List[Pokemon], tags=["Pokemon"])
def read_pokemons_by_type(type_name: str, db: PokemonDB = Depends(get_db_connection)):
    """
    Endpoint to retrieve all Pokémon of a specified type.
    """
    pokemons = get_pokemons_by_type(db, type_name)
    if not pokemons:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemons
