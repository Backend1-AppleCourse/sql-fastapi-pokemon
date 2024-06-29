from fastapi import APIRouter, HTTPException
from app.crud.pokemon_crud import get_pokemons_by_type, get_pokemons_by_trainer_name, create_pokemon, delete_pokemon_of_trainer
from app.models.pokemon import PokemonCreate

router = APIRouter()

@router.get("/type/{type_name}")
def read_pokemon_by_type(type_name: str):
    try:
        pokemons = get_pokemons_by_type(type_name)
        return pokemons
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/trainer/{trainer_name}")
def read_pokemons_by_trainer_name(trainer_name: str):
    try:
        pokemons = get_pokemons_by_trainer_name(trainer_name)
        return pokemons
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=PokemonCreate, status_code=201)
def add_pokemon(pokemon_data: PokemonCreate):
    try:
        return create_pokemon(pokemon_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{trainer_name}/{pokemon_name}", status_code=204)
def remove_pokemon_of_trainer(trainer_name: str, pokemon_name: str):
    try:
        return delete_pokemon_of_trainer(trainer_name, pokemon_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
