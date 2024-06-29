DROP DATABASE IF EXISTS pokemon_data;

-- create_tables.sql
CREATE DATABASE IF NOT EXISTS pokemon_data;

USE pokemon_data;

CREATE USER IF NOT EXISTS 'developer'@'%' IDENTIFIED BY 'html4826';
GRANT ALL PRIVILEGES ON pokemon_data.* TO 'developer'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS Trainers (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    Town varchar(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Pokemons (
    ID int NOT NULL,
    -- ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    Height decimal(5, 1),
    Weight decimal(5, 1),
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Ownerships (
    ID int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (ID),
    TrainerID int,
    PokemonID int,
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
    PRIMARY KEY (ID),
    PokemonID int,
    TypeID int,
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
