import requests
from app.models.trade import TradeRequest, TradeResponse

FASTAPI_HOST = "fastapi-container"
FASTAPI_PORT = "8000"
BASE_URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}/api/v1/trade"

def create_trade(trade_request: TradeRequest) -> TradeResponse:
    """Create a new trade request."""
    # post request to {BASE_URL}/request/
    response = requests.post(f"{BASE_URL}/request", json=trade_request.dict())
    if response.status_code != 200:
        raise Exception(response.json().get("detail"))
    return response.json()
    

def update_trade_status(trade_id: int, status: str) -> TradeResponse:
    """Update the status of an existing trade."""
    # post request to {BASE_URL}/update/
    response = requests.post(f"{BASE_URL}/{status}/{trade_id}")
    if response.status_code != 200:
        raise Exception(response.json().get("detail"))
    return response.json()
    

def get_trade_history(trainer_id: int):
    """Retrieve the trade history for a specific trainer."""
    response = requests.get(f"{BASE_URL}/history/{trainer_id}")
    if response.status_code != 200:
        raise Exception(response.json().get("detail"))
    return response.json()
    
