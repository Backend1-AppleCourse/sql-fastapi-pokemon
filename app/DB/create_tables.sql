CREATE DATABASE IF NOT EXISTS pokemon_data;

USE pokemon_data;

CREATE TABLE IF NOT EXISTS Trainers (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    Town varchar(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Pokemons (
    ID int NOT NULL,
    Name varchar(255) NOT NULL,
    Height decimal(5, 1),
    Weight decimal(5, 1),
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Ownerships (
    ID int NOT NULL AUTO_INCREMENT,
    TrainerID int,
    PokemonID int,
    PRIMARY KEY (ID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(ID) ON DELETE CASCADE,
    FOREIGN KEY (PokemonID) REFERENCES Pokemons(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Types (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Pokemon_Types (
    ID int NOT NULL AUTO_INCREMENT,
    PokemonID int,
    TypeID int,
    PRIMARY KEY (ID),
    FOREIGN KEY (PokemonID) REFERENCES Pokemons(ID) ON DELETE CASCADE,
    FOREIGN KEY (TypeID) REFERENCES Types(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Trades (
    ID int NOT NULL AUTO_INCREMENT,
    InitiatorTrainerID int,
    ReceiverTrainerID int,
    InitiatorPokemonID int,
    ReceiverPokemonID int,
    Status varchar(50) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ID),
    FOREIGN KEY (InitiatorTrainerID) REFERENCES Trainers(ID) ON DELETE CASCADE,
    FOREIGN KEY (ReceiverTrainerID) REFERENCES Trainers(ID) ON DELETE CASCADE,
    FOREIGN KEY (InitiatorPokemonID) REFERENCES Pokemons(ID) ON DELETE CASCADE,
    FOREIGN KEY (ReceiverPokemonID) REFERENCES Pokemons(ID) ON DELETE CASCADE
);
