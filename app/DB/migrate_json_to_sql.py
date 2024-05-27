import json
import pymysql
import traceback  # Import the traceback module

# Database connection setup
def get_db_connection():
    return pymysql.connect(host='localhost',
                           port=3000,
                           user='developer',
                           password='html4826',
                           db='pokemon_data',
                           cursorclass=pymysql.cursors.DictCursor)

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def insert_data(data):
    db = get_db_connection()
    try:
        with db.cursor() as cursor:
            trainers = {}
            types = {}

            for pokemon in data:
                # Check if type is a list or a single string and standardize to list
                pokemon_types = pokemon['type'] if isinstance(pokemon['type'], list) else [pokemon['type']]

                # Insert Pokémon using the ID from the JSON data
                cursor.execute('INSERT INTO Pokemons (ID, Name, Height, Weight) VALUES (%s, %s, %s, %s)',
                               (pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight']))
                db.commit()

                # Handle multiple types
                for type_name in pokemon_types:
                    if type_name not in types:
                        cursor.execute('INSERT INTO Types (Name) VALUES (%s)', (type_name,))
                        db.commit()
                        types[type_name] = cursor.lastrowid
                    
                    cursor.execute('INSERT INTO Pokemon_Types (PokemonID, TypeID) VALUES (%s, %s)',
                                   (pokemon['id'], types[type_name]))

                # Handle ownerships
                for owner in pokemon['ownedBy']:
                    trainer_key = (owner['name'], owner['town'])
                    if trainer_key not in trainers:
                        cursor.execute('INSERT INTO Trainers (Name, Town) VALUES (%s, %s)', (owner['name'], owner['town']))
                        db.commit()
                        trainers[trainer_key] = cursor.lastrowid

                    cursor.execute('INSERT INTO Ownerships (TrainerID, PokemonID) VALUES (%s, %s)', (trainers[trainer_key], pokemon['id']))
                db.commit()

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    pokemon_data = load_data('pokemons_data.json')
    insert_data(pokemon_data)