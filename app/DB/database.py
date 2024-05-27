# database.py
import pymysql
from .pokemon_queries import get_pokemon_by_type_query, get_pokemons_by_trainer_name_query
from .trainer_queries import get_trainers_by_pokemon_name_query

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
