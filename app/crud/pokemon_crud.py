
# pokemon_crud.py
from app.DB.database import PokemonDB
from app.schemas.pokemon import PokemonCreate

def get_pokemons_by_type(db: PokemonDB, type_name: str):
    """Retrieve all pokemons by their type."""
    print("in get_pokemons_by_type")
    return db.get_pokemon_by_type(type_name)

def get_pokemons_by_trainer_name(db: PokemonDB, trainer_name: str):
    """Retrieve all pokemons by their type."""
    print("in get_pokemons_by_type")
    return db.get_pokemons_by_trainer_name(trainer_name)

def create_pokemon(db: PokemonDB, pokemon_data: PokemonCreate):
    db.add_pokemon(pokemon_data)

def delete_pokemon_of_trainer(db: PokemonDB, trainer_name: str, pokemon_name: str):
    db.delete_pokemon_of_trainer(trainer_name, pokemon_name)
