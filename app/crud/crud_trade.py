from app.DB.database import PokemonDB
from app.schemas.trade import TradeRequest, TradeResponse

def create_trade(db: PokemonDB, trade_request: TradeRequest) -> TradeResponse:
    """Create a new trade request."""
    print("Creating trade")
    trade_id = db.create_trade(trade_request)
    return db.get_trade_by_id(trade_id)

def update_trade_status(db: PokemonDB, trade_id: int, status: str) -> TradeResponse:
    """Update the status of an existing trade."""
    print(f"Updating trade status to {status}")
    db.update_trade_status(trade_id, status)
    return db.get_trade_by_id(trade_id)

def get_trade_by_id(db: PokemonDB, trade_id: int) -> TradeResponse:
    """Retrieve a trade by its ID."""
    print(f"Fetching trade with ID {trade_id}")
    return db.get_trade_by_id(trade_id)

def get_trade_history(db: PokemonDB, trainer_id: int):
    """Retrieve the trade history for a specific trainer."""
    print(f"Fetching trade history for Trainer ID {trainer_id}")
    return db.get_trade_history(trainer_id)
