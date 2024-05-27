

def get_trainers_by_pokemon_name_query():
    return """
    SELECT Trainers.Name AS TrainerName, Trainers.Town
    FROM Trainers
    INNER JOIN Ownerships ON Trainers.ID = Ownerships.TrainerID
    INNER JOIN Pokemons ON Ownerships.PokemonID = Pokemons.ID
    WHERE Pokemons.Name = %s;
    """