from fastapi import APIRouter, Depends, HTTPException
from app.models.trade import TradeRequest, TradeResponse
from app.crud import crud_trade
from typing import List

router = APIRouter()

def get_db():
    return get_db_connection()

@router.post("/request", response_model=TradeResponse)
def request_trade(trade_request: TradeRequest):
    trade = crud_trade.create_trade(trade_request)
    return trade

@router.post("/accept/{trade_id}", response_model=TradeResponse)
def accept_trade(trade_id: int):
    trade = crud_trade.update_trade_status(trade_id, 'accept')
    return trade

@router.post("/reject/{trade_id}", response_model=TradeResponse)
def reject_trade(trade_id: int):
    trade = crud_trade.update_trade_status(trade_id, 'reject')
    return trade

@router.post("/cancel/{trade_id}", response_model=TradeResponse)
def cancel_trade(trade_id: int):
    trade = crud_trade.update_trade_status(trade_id, 'cancel')
    return trade

@router.get("/history/{trainer_id}", response_model=List[TradeResponse])
def trade_history(trainer_id: int):
    history = crud_trade.get_trade_history(trainer_id)
    return history
