# database.py
import pymysql
from .pokemon_queries import get_pokemon_by_type_query, get_pokemons_by_trainer_name_query
from .trainer_queries import get_trainers_by_pokemon_name_query
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
