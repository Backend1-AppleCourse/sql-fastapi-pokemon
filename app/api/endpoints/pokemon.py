# pokemon.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...db.database import PokemonDB, get_db_connection
from ...crud.pokemon_crud import get_pokemons_by_type
from ...schemas.pokemon import Pokemon

router = APIRouter()

@router.get("/by-type/{type_name}")
def read_pokemon_by_type(type_name: str, db=Depends(get_db_connection)):
    pokemons = get_pokemons_by_type(db, type_name)
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokémon found with the given type")
    return pokemons
