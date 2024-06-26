import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.DB.database import PokemonDB, get_db_connection
from app.crud.trainer_crud import get_trainers_by_pokemon_name, add_pokemon_to_trainer_by_name, evolve_pokemon
from app.schemas.trainer import TrainerPokemonRequest, TrainerPokemonResponse  # Assuming you have a schema for this

router = APIRouter()

@router.get("/by-pokemon/{pokemon_name}")
def read_pokemon_by_type(pokemon_name: str, db=Depends(get_db_connection)):
    trainers = get_trainers_by_pokemon_name(db, pokemon_name)
    if not trainers:
        raise HTTPException(status_code=404, detail="No Pokémon found with the given type")
    return trainers

@router.post("/add-pokemon/", response_model=TrainerPokemonResponse, status_code=201)
def api_add_pokemon_to_trainer(data: TrainerPokemonRequest, db=Depends(get_db_connection)):
    try:
        add_pokemon_to_trainer_by_name(db, data.trainer_name, data.pokemon_name)
        return {
            "message": "Pokémon successfully added to trainer",
            "trainer_name": data.trainer_name,
            "pokemon_name": data.pokemon_name
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")

@router.post("/evolve-pokemon/", response_model=TrainerPokemonResponse, status_code=201)
def api_evolve_pokemon(data: TrainerPokemonRequest, db=Depends(get_db_connection)):
    try:
        evolve_pokemon(db, data.trainer_name, data.pokemon_name)
        return {
            "message": "Pokémon successfully evolved",
            "trainer_name": data.trainer_name,
            "pokemon_name": data.pokemon_name
        }
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Server error")