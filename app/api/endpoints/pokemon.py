# pokemon.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...db.database import PokemonDB, get_db_connection
from ...crud.pokemon_crud import get_pokemons_by_type, get_pokemons_by_trainer_name, create_pokemon, delete_pokemon_of_trainer
from ...schemas.pokemon import PokemonCreate

router = APIRouter()

@router.get("/by-type/{type_name}")
def read_pokemon_by_type(type_name: str, db=Depends(get_db_connection)):
    pokemons = get_pokemons_by_type(db, type_name)
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokémon found with the given type")
    return pokemons

@router.get("/by-trainer-name/{trainer_name}")
def read_pokemons_by_trainer_name(trainer_name: str, db=Depends(get_db_connection)):
    pokemons = get_pokemons_by_trainer_name(db, trainer_name)
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokémon found with the given type")
    return pokemons

@router.post("/pokemon/", response_model=PokemonCreate, status_code=201)
def add_pokemon(pokemon_data: PokemonCreate, db: PokemonDB = Depends(get_db_connection)):
    try:
        create_pokemon(db, pokemon_data)
        return pokemon_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/trainer/{trainer_name}/pokemon/{pokemon_name}", status_code=204)
def remove_pokemon_of_trainer(trainer_name: str, pokemon_name: str, db=Depends(get_db_connection)):
    try:
        delete_pokemon_of_trainer(db, trainer_name, pokemon_name)
        return {"message": "Pokemon successfully deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")