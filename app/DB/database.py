import requests
import pymysql
from app.DB.pokemon_queries import get_pokemon_by_type_query, get_pokemons_by_trainer_name_query, \
    delete_pokemon_of_trainer_query
from app.DB.trainer_queries import get_trainers_by_pokemon_name_query, add_pokemon_to_trainer_by_name_query, \
    update_ownership_query, add_evolved_pokemon_query, check_ownership_query
from app.DB.trade_queries import create_trade_query, update_trade_status_query, get_trade_by_id_query, \
    get_trade_history_query
from app.schemas.pokemon import PokemonCreate
from app.schemas.trade import TradeRequest, TradeResponse


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
            cursor.execute(
                "INSERT INTO Pokemons (ID, Name, Height, Weight) VALUES (%s, %s, %s, %s)",
                (pokemon_data.id, pokemon_data.name, pokemon_data.height, pokemon_data.weight)
            )
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
            cursor.execute(check_ownership_query(), (trainer_name, pokemon_name))
            result = cursor.fetchone()
            if result['count'] == 0:
                raise ValueError("Trainer does not own this Pokémon or Pokémon does not exist.")

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

            evolved_pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{evolved_pokemon_name}/")
            evolved_pokemon_response.raise_for_status()
            evolved_pokemon_data = evolved_pokemon_response.json()

            evolved_pokemon_id = evolved_pokemon_data['id']
            evolved_pokemon_height = evolved_pokemon_data['height']
            evolved_pokemon_weight = evolved_pokemon_data['weight']

            cursor.execute(add_evolved_pokemon_query(),
                           (evolved_pokemon_id, evolved_pokemon_name, evolved_pokemon_height, evolved_pokemon_weight))
            self.connection.commit()

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

    def create_trade(self, trade_request: TradeRequest):
        query = create_trade_query()
        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                trade_request.initiator_trainer_id,
                trade_request.receiver_trainer_id,
                trade_request.initiator_pokemon_id,
                trade_request.receiver_pokemon_id
            ))
            self.connection.commit()
            trade_id = cursor.lastrowid
        return trade_id

    def update_trade_status(self, trade_id: int, status: str):
        query = update_trade_status_query()
        with self.connection.cursor() as cursor:
            cursor.execute(query, (status, trade_id))
            self.connection.commit()

    def get_trade_by_id(self, trade_id: int) -> TradeResponse:
        query = get_trade_by_id_query()
        with self.connection.cursor() as cursor:
            cursor.execute(query, (trade_id,))
            result = cursor.fetchone()
        if not result:
            raise ValueError("Trade not found")
        return TradeResponse(
            id=result['ID'],
            initiator_trainer_id=result['InitiatorTrainerID'],
            receiver_trainer_id=result['ReceiverTrainerID'],
            initiator_pokemon_id=result['InitiatorPokemonID'],
            receiver_pokemon_id=result['ReceiverPokemonID'],
            status=result['Status']
        )

    def get_trade_history(self, trainer_id: int):
        query = get_trade_history_query()
        with self.connection.cursor() as cursor:
            cursor.execute(query, (trainer_id, trainer_id))
            results = cursor.fetchall()
        return [TradeResponse(
            id=result['ID'],
            initiator_trainer_id=result['InitiatorTrainerID'],
            receiver_trainer_id=result['ReceiverTrainerID'],
            initiator_pokemon_id=result['InitiatorPokemonID'],
            receiver_pokemon_id=result['ReceiverPokemonID'],
            status=result['Status']
        ) for result in results]


def get_db_connection():
    connection_params = {
        'host': 'localhost',
        'port': 3000,
        'user': 'root',
        'password': '123456789',
        'database': 'pokemon_data',
        'cursorclass': pymysql.cursors.DictCursor
    }
    connection = pymysql.connect(**connection_params)
    return PokemonDB(connection)