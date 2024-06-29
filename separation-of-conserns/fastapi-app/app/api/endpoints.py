from fastapi import APIRouter, HTTPException, Depends
from app.db.database import get_db_connection, PokemonDB
from typing import List
from app.schemas.pokemon import PokemonCreate
from app.schemas.trainer import TrainerPokemonResponse, TrainerPokemonRequest
from app.schemas.trade import TradeRequest, TradeResponse

router = APIRouter()

@router.get("/pokemons/type/{type_name}")
def get_pokemons_by_type(type_name: str):
    db: PokemonDB = get_db_connection()
    try:
        pokemons = db.get_pokemon_by_type(type_name)
        if not pokemons:
            raise HTTPException(status_code=404, detail="Pokemons not found")
        return pokemons
    finally:
        db.connection.close()

@router.get("/trainers/pokemon/{pokemon_name}")
def get_trainers_by_pokemon_name(pokemon_name: str):
    db: PokemonDB = get_db_connection()
    try:
        trainers = db.get_trainer_by_pokemon_name(pokemon_name)
        if not trainers:
            raise HTTPException(status_code=404, detail="Trainers not found")
        return trainers
    finally:
        db.connection.close()

@router.get("/pokemons/trainer/{trainer_name}")
def get_pokemons_by_trainer_name(trainer_name: str):
    db: PokemonDB = get_db_connection()
    try:
        pokemons = db.get_pokemons_by_trainer_name(trainer_name)
        if not pokemons:
            raise HTTPException(status_code=404, detail="Pokemons not found")
        return pokemons
    finally:
        db.connection.close()

@router.post("/pokemons/")
def add_pokemon(pokemon_data: PokemonCreate):
    db: PokemonDB = get_db_connection()
    try:
        db.add_pokemon(pokemon_data)
        return {"message": "Pokemon added successfully"}
    finally:
        db.connection.close()

@router.delete("/pokemons/trainer/{trainer_name}/{pokemon_name}")
def delete_pokemon_of_trainer(trainer_name: str, pokemon_name: str):
    db: PokemonDB = get_db_connection()
    try:
        db.delete_pokemon_of_trainer(trainer_name, pokemon_name)
        return {"message": "Pokemon deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        db.connection.close()

@router.post("/trainers/{trainer_name}/pokemons/{pokemon_name}")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
    db: PokemonDB = get_db_connection()
    try:
        db.add_pokemon_to_trainer_by_name(trainer_name, pokemon_name)
        return {"message": "Pokemon assigned to trainer successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.connection.close()

@router.post("/trainers/{trainer_name}/pokemons/{pokemon_name}/evolve")
def evolve_pokemon(trainer_name: str, pokemon_name: str):
    db: PokemonDB = get_db_connection()
    try:
        db.evolve_pokemon(trainer_name, pokemon_name)
        return {"message": "Pokemon evolved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.connection.close()

@router.post("/trade/request", response_model=TradeResponse)
def request_trade(trade_request: TradeRequest, db: PokemonDB = Depends(get_db_connection)):
    """Create a new trade request."""
    print("Creating trade")
    trade_id = db.create_trade(trade_request)
    return db.get_trade_by_id(trade_id)

@router.post("/trade/accept/{trade_id}", response_model=TradeResponse)
def accept_trade(trade_id: int, db: PokemonDB = Depends(get_db_connection)):
    """Update the status of an existing trade."""
    print(f"Updating trade status to accepted")
    db.update_trade_status(trade_id, 'accepted')
    return db.get_trade_by_id(trade_id)

@router.post("/trade/reject/{trade_id}", response_model=TradeResponse)
def reject_trade(trade_id: int, db: PokemonDB = Depends(get_db_connection)):
    """Update the status of an existing trade."""
    print(f"Updating trade status to rejected")
    db.update_trade_status(trade_id, 'rejected')
    return db.get_trade_by_id(trade_id)

@router.post("/trade/cancel/{trade_id}", response_model=TradeResponse)
def cancel_trade(trade_id: int, db: PokemonDB = Depends(get_db_connection)):
    """Update the status of an existing trade."""
    print(f"Updating trade status to canceled")
    db.update_trade_status(trade_id, 'canceled')
    return db.get_trade_by_id(trade_id)

@router.get("/trade/history/{trainer_id}", response_model=List[TradeResponse])
def trade_history(trainer_id: int, db: PokemonDB = Depends(get_db_connection)):
    """Retrieve the trade history for a specific trainer."""
    print(f"Fetching trade history for Trainer ID {trainer_id}")
    return db.get_trade_history(trainer_id)
