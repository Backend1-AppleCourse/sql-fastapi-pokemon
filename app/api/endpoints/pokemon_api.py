# File: /app/api/endpoints/pokemon.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...db.deps import get_db
from ...schemas.pokemon import Pokemon, PokemonCreate  # Assuming you have defined these Pydantic models
from pokemon.crud import get_pokemon_by_id

router = APIRouter()

@router.get("/pokemons/{pokemon_id}")
def read_pokemons_by_type(pokemon_id: int):
    pokemon = get_pokemon_by_id(pokemon_id)
    if(pokemon != None):
        return pokemon
    raise HTTPException(status_code=404, detail="Pokémon not found")
