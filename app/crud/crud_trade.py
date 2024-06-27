from app.schemas.trade import TradeRequest, TradeResponse
from app.DB.database import PokemonDB
from fastapi import HTTPException
import logging

# Create Trade
def create_trade(db: PokemonDB, trade_request: TradeRequest) -> TradeResponse:
    try:
        logging.info(f"Creating trade with request: {trade_request}")
        sql = """
        INSERT INTO Trades (InitiatorTrainerID, ReceiverTrainerID, InitiatorPokemonID, ReceiverPokemonID, Status, CreatedAt, UpdatedAt)
        VALUES (%s, %s, %s, %s, 'pending', NOW(), NOW())
        """
        with db.connection.cursor() as cursor:
            cursor.execute(sql, (
                trade_request.initiator_trainer_id,
                trade_request.receiver_trainer_id,
                trade_request.initiator_pokemon_id,
                trade_request.receiver_pokemon_id
            ))
            db.connection.commit()
            trade_id = cursor.lastrowid

        logging.info(f"Trade created successfully. Trade ID: {trade_id}")

        return TradeResponse(
            id=trade_id,
            initiator_trainer_id=trade_request.initiator_trainer_id,
            receiver_trainer_id=trade_request.receiver_trainer_id,
            initiator_pokemon_id=trade_request.initiator_pokemon_id,
            receiver_pokemon_id=trade_request.receiver_pokemon_id,
            status='pending'
        )
    except Exception as e:
        logging.error(f"Error creating trade: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Update Trade Status
def update_trade_status(db: PokemonDB, trade_id: int, status: str) -> TradeResponse:
    try:
        logging.info(f"Updating trade status. Trade ID: {trade_id}, New Status: {status}")
        sql = "UPDATE Trades SET Status = %s, UpdatedAt = NOW() WHERE ID = %s"
        with db.connection.cursor() as cursor:
            cursor.execute(sql, (status, trade_id))
            db.connection.commit()

        trade = get_trade_by_id(db, trade_id)
        logging.info(f"Trade status updated successfully. Trade ID: {trade.id}, Status: {trade.status}")
        return trade
    except Exception as e:
        logging.error(f"Error updating trade status: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get Trade by ID
def get_trade_by_id(db: PokemonDB, trade_id: int) -> TradeResponse:
    try:
        logging.info(f"Fetching trade by ID: {trade_id}")
        sql = "SELECT * FROM Trades WHERE ID = %s"
        with db.connection.cursor() as cursor:
            cursor.execute(sql, (trade_id,))
            result = cursor.fetchone()

        if not result:
            logging.warning(f"Trade not found. Trade ID: {trade_id}")
            raise HTTPException(status_code=404, detail="Trade not found")

        logging.info(f"Trade fetched successfully. Trade ID: {result['ID']}")

        return TradeResponse(
            id=result['ID'],
            initiator_trainer_id=result['InitiatorTrainerID'],
            receiver_trainer_id=result['ReceiverTrainerID'],
            initiator_pokemon_id=result['InitiatorPokemonID'],
            receiver_pokemon_id=result['ReceiverPokemonID'],
            status=result['Status']
        )
    except Exception as e:
        logging.error(f"Error fetching trade by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get Trade History
def get_trade_history(db: PokemonDB, trainer_id: int):
    try:
        logging.info(f"Fetching trade history for Trainer ID: {trainer_id}")
        sql = """
        SELECT * FROM Trades
        WHERE InitiatorTrainerID = %s OR ReceiverTrainerID = %s
        ORDER BY ID DESC
        """
        with db.connection.cursor() as cursor:
            cursor.execute(sql, (trainer_id, trainer_id))
            results = cursor.fetchall()

        logging.info(f"Trade history fetched successfully for Trainer ID: {trainer_id}")

        return [TradeResponse(
            id=result['ID'],
            initiator_trainer_id=result['InitiatorTrainerID'],
            receiver_trainer_id=result['ReceiverTrainerID'],
            initiator_pokemon_id=result['InitiatorPokemonID'],
            receiver_pokemon_id=result['ReceiverPokemonID'],
            status=result['Status']
        ) for result in results]
    except Exception as e:
        logging.error(f"Error fetching trade history: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
