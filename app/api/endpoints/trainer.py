
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...db.database import PokemonDB, get_db_connection
from ...crud.trainer_crud import get_trainers_by_pokemon_name
from ...schemas.trainer import Trainer

router = APIRouter()

@router.get("/by-pokemon/{pokemon_name}")
def read_pokemon_by_type(pokemon_name: str, db=Depends(get_db_connection)):
    trainers = get_trainers_by_pokemon_name(db, pokemon_name)
    if not trainers:
        raise HTTPException(status_code=404, detail="No Pokémon found with the given type")
    return trainers
