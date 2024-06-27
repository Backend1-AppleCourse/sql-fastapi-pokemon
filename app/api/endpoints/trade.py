from fastapi import APIRouter, Depends, HTTPException
from app.schemas.trade import TradeRequest, TradeResponse
from app.crud import crud_trade
from app.DB.database import get_db_connection, PokemonDB
from typing import List

router = APIRouter()

def get_db():
    return get_db_connection()

@router.post("/request", response_model=TradeResponse)
def request_trade(trade_request: TradeRequest, db: PokemonDB = Depends(get_db)):
    trade = crud_trade.create_trade(db, trade_request)
    return trade

@router.post("/accept/{trade_id}", response_model=TradeResponse)
def accept_trade(trade_id: int, db: PokemonDB = Depends(get_db)):
    trade = crud_trade.update_trade_status(db, trade_id, 'accepted')
    return trade

@router.post("/reject/{trade_id}", response_model=TradeResponse)
def reject_trade(trade_id: int, db: PokemonDB = Depends(get_db)):
    trade = crud_trade.update_trade_status(db, trade_id, 'rejected')
    return trade

@router.post("/cancel/{trade_id}", response_model=TradeResponse)
def cancel_trade(trade_id: int, db: PokemonDB = Depends(get_db)):
    trade = crud_trade.update_trade_status(db, trade_id, 'cancelled')
    return trade

@router.get("/history/{trainer_id}", response_model=List[TradeResponse])
def trade_history(trainer_id: int, db: PokemonDB = Depends(get_db)):
    history = crud_trade.get_trade_history(db, trainer_id)
    return history
