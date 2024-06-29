import logging
from fastapi import APIRouter, HTTPException
from app.crud.trainer_crud import get_trainers_by_pokemon_name, add_pokemon_to_trainer_by_name, evolve_pokemon
from app.models.trainer import TrainerPokemonRequest, TrainerPokemonResponse

router = APIRouter()

@router.get("/by-pokemon/{pokemon_name}")
def read_pokemon_by_type(pokemon_name: str):
    try:
        trainers = get_trainers_by_pokemon_name(pokemon_name)
        return trainers
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/add-pokemon/", response_model=TrainerPokemonResponse, status_code=201)
def api_add_pokemon_to_trainer(data: TrainerPokemonRequest):
    try:
        return add_pokemon_to_trainer_by_name(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/evolve-pokemon/", response_model=TrainerPokemonResponse, status_code=201)
def api_evolve_pokemon(data: TrainerPokemonRequest):
    try:
        return evolve_pokemon(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
