import requests
from app.models.trainer import TrainerPokemonRequest

FASTAPI_HOST = "fastapi-container"
FASTAPI_PORT = "8000"
BASE_URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}/api/v1"

def get_trainers_by_pokemon_name(pokemon_name: str):
    response = requests.get(f"{BASE_URL}/trainers/pokemon/{pokemon_name}")
    if response.status_code != 200:
        raise Exception(response.json().get("detail"))
    return response.json()

def add_pokemon_to_trainer_by_name(data: TrainerPokemonRequest):
    response = requests.post(f"{BASE_URL}/trainers/add-pokemon/", json=data.dict())
    if response.status_code != 201:
        raise Exception(response.json().get("detail"))
    return response.json()

def evolve_pokemon(data: TrainerPokemonRequest):
    response = requests.post(f"{BASE_URL}/trainers/evolve-pokemon/", json=data.dict())
    if response.status_code != 201:
        raise Exception(response.json().get("detail"))
    return response.json()
