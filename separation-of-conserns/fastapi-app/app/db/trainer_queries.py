
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

def check_ownership_query():
    return """
    SELECT COUNT(*) as count
    FROM Ownerships o
    JOIN Trainers t ON o.TrainerID = t.ID
    JOIN Pokemons p ON o.PokemonID = p.ID
    WHERE t.Name = %s AND p.Name = %s;
    """

def get_pokemon_by_type_query():
    return """
    SELECT Pokemons.Name, Types.Name AS TypeName
    FROM Pokemons
    JOIN Pokemon_Types ON Pokemons.ID = Pokemon_Types.PokemonID
    JOIN Types ON Pokemon_Types.TypeID = Types.ID
    WHERE Types.Name = %s;
    """

def add_evolved_pokemon_query():
    return """
    INSERT INTO Pokemons (ID, Name, Height, Weight) VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE Name=VALUES(Name), Height=VALUES(Height), Weight=VALUES(Weight);
    """

def update_ownership_query():
    return """
    UPDATE Ownerships
    SET PokemonID = %s
    WHERE TrainerID = (SELECT ID FROM Trainers WHERE Name = %s)
    AND PokemonID = (SELECT ID FROM Pokemons WHERE Name = %s);
    """

def add_pokemon_type_query():
    return """
    INSERT INTO Pokemon_Types (PokemonID, TypeID)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE PokemonID=VALUES(PokemonID), TypeID=VALUES(TypeID);
    """

def add_type_query():
    return """
    INSERT INTO Types (Name) VALUES (%s)
    ON DUPLICATE KEY UPDATE Name=Name;
    """

def get_type_id_query():
    return """
    SELECT ID FROM Types WHERE Name = %s;
    """

