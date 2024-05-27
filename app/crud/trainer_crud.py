
# pokemon_crud.py
from ..db.database import PokemonDB

def get_trainers_by_pokemon_name(db: PokemonDB, pokemon_name: str):
    """Retrieve all pokemons by their type."""
    print("in get_trainer_by_pokemon_name")
    return db.get_trainer_by_pokemon_name(pokemon_name)

def add_pokemon_to_trainer_by_name(db: PokemonDB, trainer_name: str, pokemon_name: str):
    db.add_pokemon_to_trainer_by_name(trainer_name, pokemon_name)
