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
