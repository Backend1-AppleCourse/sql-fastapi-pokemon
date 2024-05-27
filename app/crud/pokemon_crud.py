
# pokemon_crud.py
from ..db.database import PokemonDB

def get_pokemons_by_type(db: PokemonDB, type_name: str):
    """Retrieve all pokemons by their type."""
    print("in get_pokemons_by_type")
    return db.get_pokemon_by_type(type_name)

def get_pokemons_by_trainer_name(db: PokemonDB, trainer_name: str):
    """Retrieve all pokemons by their type."""
    print("in get_pokemons_by_type")
    return db.get_pokemons_by_trainer_name(trainer_name)
