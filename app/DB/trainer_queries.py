
def get_trainers_by_pokemon_name_query():
    return """
    SELECT Trainers.Name AS TrainerName, Trainers.Town
    FROM Trainers
    INNER JOIN Ownerships ON Trainers.ID = Ownerships.TrainerID
    INNER JOIN Pokemons ON Ownerships.PokemonID = Pokemons.ID
    WHERE Pokemons.Name = %s;
    """

def add_pokemon_to_trainer_by_name_query():
    return """
    INSERT INTO Ownerships (TrainerID, PokemonID)
    SELECT t.ID, p.ID
    FROM Trainers t
    JOIN Pokemons p ON t.Name = %s AND p.Name = %s
    WHERE NOT EXISTS (
        SELECT 1 FROM Ownerships o WHERE o.TrainerID = t.ID AND o.PokemonID = p.ID
    );
    """

