import requests
from app.models.pokemon import PokemonCreate

FASTAPI_HOST = "fastapi-container"
FASTAPI_PORT = "8000"
BASE_URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}/api/v1"

def get_pokemons_by_type(type_name: str):
    response = requests.get(f"{BASE_URL}/pokemons/type/{type_name}")
    if response.status_code != 200:
        raise Exception(response.json().get("detail"))
    return response.json()

def get_pokemons_by_trainer_name(trainer_name: str):
    response = requests.get(f"{BASE_URL}/pokemons/trainer/{trainer_name}")
    if response.status_code != 200:
        raise Exception(response.json().get("detail"))
    return response.json()

def create_pokemon(pokemon_data: PokemonCreate):
    response = requests.post(f"{BASE_URL}/pokemons/", json=pokemon_data.dict())
    if response.status_code != 201:
        raise Exception(response.json().get("detail"))
    return response.json()

def delete_pokemon_of_trainer(trainer_name: str, pokemon_name: str):
    response = requests.delete(f"{BASE_URL}/pokemons/trainer/{trainer_name}/{pokemon_name}")
    if response.status_code != 204:
        raise Exception(response.json().get("detail"))
    return {"message": "Pokemon successfully deleted"}
