# database.py
import requests
import pymysql
from .pokemon_queries import get_pokemon_by_type_query, get_pokemons_by_trainer_name_query, delete_pokemon_of_trainer_query
from .trainer_queries import get_trainers_by_pokemon_name_query, add_pokemon_to_trainer_by_name_query, update_ownership_query, add_evolved_pokemon_query, check_ownership_query
from ..schemas.pokemon import PokemonCreate

class PokemonDB:
    def __init__(self, connection):
        self.connection = connection

    def get_pokemon_by_type(self, type_name):
        with self.connection.cursor() as cursor:
            cursor.execute(get_pokemon_by_type_query(), (type_name,))
            return cursor.fetchall()

    def get_trainer_by_pokemon_name(self, pokemon_name):
        with self.connection.cursor() as cursor:
            cursor.execute(get_trainers_by_pokemon_name_query(), (pokemon_name,))
            return cursor.fetchall()

    def get_pokemons_by_trainer_name(self, trainer_name):
        with self.connection.cursor() as cursor:
            cursor.execute(get_pokemons_by_trainer_name_query(), (trainer_name,))
            return cursor.fetchall()
    
    def add_pokemon(self, pokemon_data: PokemonCreate):
        with self.connection.cursor() as cursor:
            # Insert the main Pokémon details
            cursor.execute(
                "INSERT INTO Pokemons (ID, Name, Height, Weight) VALUES (%s, %s, %s, %s)",
                (pokemon_data.id, pokemon_data.name, pokemon_data.height, pokemon_data.weight)
            )
            # Insert each type into the Types table and create associations in Pokemon_Types
            for type_name in pokemon_data.types:
                cursor.execute("INSERT IGNORE INTO Types (Name) VALUES (%s)", (type_name,))
                cursor.execute("INSERT INTO Pokemon_Types (PokemonID, TypeID) SELECT %s, ID FROM Types WHERE Name = %s", 
                               (pokemon_data.id, type_name))
            self.connection.commit()

    def delete_pokemon_of_trainer(self, trainer_name: str, pokemon_name: str):
        query = delete_pokemon_of_trainer_query()
        with self.connection.cursor() as cursor:
            cursor.execute(query, (trainer_name, pokemon_name))
            self.connection.commit()
            if cursor.rowcount == 0:
                raise ValueError("No such ownership exists")
    
    def add_pokemon_to_trainer_by_name(self, trainer_name: str, pokemon_name: str):
        query = add_pokemon_to_trainer_by_name_query()
        with self.connection.cursor() as cursor:
            cursor.execute(query, (trainer_name, pokemon_name))
            self.connection.commit()
            if cursor.rowcount == 0:
                raise ValueError("This Pokémon is already assigned to this trainer or the names are incorrect.")

    def evolve_pokemon(self, trainer_name: str, pokemon_name: str):
        with self.connection.cursor() as cursor:
            # Check ownership
            cursor.execute(check_ownership_query(), (trainer_name, pokemon_name))
            result = cursor.fetchone()
            if result['count'] == 0:
                raise ValueError("Trainer does not own this Pokémon or Pokémon does not exist.")
            
            # Get evolution details from external API
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/")
            response.raise_for_status()
            species_data = response.json()
            evolution_chain_url = species_data['evolution_chain']['url']

            evolution_chain_response = requests.get(evolution_chain_url)
            evolution_chain_response.raise_for_status()
            evolution_chain_data = evolution_chain_response.json()

            evolved_pokemon_name = self.find_evolved_pokemon(evolution_chain_data, pokemon_name.lower())
            if not evolved_pokemon_name:
                raise ValueError("No evolution found for this Pokémon.")

            # Get evolved Pokémon details from external API
            evolved_pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{evolved_pokemon_name}/")
            evolved_pokemon_response.raise_for_status()
            evolved_pokemon_data = evolved_pokemon_response.json()

            evolved_pokemon_id = evolved_pokemon_data['id']
            evolved_pokemon_height = evolved_pokemon_data['height']
            evolved_pokemon_weight = evolved_pokemon_data['weight']

            # Add evolved Pokémon to the database
            cursor.execute(add_evolved_pokemon_query(), (evolved_pokemon_id, evolved_pokemon_name, evolved_pokemon_height, evolved_pokemon_weight))
            self.connection.commit()

            # Update ownership
            cursor.execute(update_ownership_query(), (evolved_pokemon_id, trainer_name, pokemon_name))
            self.connection.commit()

    def find_evolved_pokemon(self, evolution_chain, current_pokemon):
        chain = evolution_chain['chain']
        return self.traverse_evolution_chain(chain, current_pokemon)

    def traverse_evolution_chain(self, chain, current_pokemon):
        if chain['species']['name'] == current_pokemon:
            if chain['evolves_to']:
                return chain['evolves_to'][0]['species']['name']
            else:
                return None
        for evolution in chain['evolves_to']:
            result = self.traverse_evolution_chain(evolution, current_pokemon)
            if result:
                return result
        return None

def get_db_connection():
    connection_params = {
        'host': 'localhost',
        'port': 3000,
        'user': 'developer',
        'password': 'html4826',
        'database': 'pokemon_data',
        'cursorclass': pymysql.cursors.DictCursor
    }
    connection = pymysql.connect(**connection_params)
    return PokemonDB(connection)
