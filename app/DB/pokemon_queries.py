# pokemon_queries.py
# Contains all SQL queries for operations related to 'Pokemons'

def get_pokemon_by_type_query():
    return """
    SELECT Pokemons.Name, Types.Name AS TypeName
    FROM Pokemons
    JOIN Pokemon_Types ON Pokemons.ID = Pokemon_Types.PokemonID
    JOIN Types ON Pokemon_Types.TypeID = Types.ID
    WHERE Types.Name = %s;
    """

def get_pokemons_by_trainer_name_query():
    return """
    SELECT Pokemons.Name
    FROM Trainers
    JOIN Ownerships ON Trainers.ID = Ownerships.TrainerID
    JOIN Pokemons ON Ownerships.PokemonID = Pokemons.ID
    WHERE Trainers.Name = %s;
    """
def delete_pokemon_of_trainer_query():
    return """
    DELETE Ownerships
    FROM Ownerships
    JOIN Trainers ON Ownerships.TrainerID = Trainers.ID
    JOIN Pokemons ON Ownerships.PokemonID = Pokemons.ID
    WHERE Trainers.Name = %s AND Pokemons.Name = %s;
    """
