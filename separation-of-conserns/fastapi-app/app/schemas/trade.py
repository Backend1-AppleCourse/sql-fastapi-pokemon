from pydantic import BaseModel
from typing import Optional

class TradeRequest(BaseModel):
    initiator_trainer_id: int
    receiver_trainer_id: int
    initiator_pokemon_id: int
    receiver_pokemon_id: Optional[int] = None

class TradeResponse(BaseModel):
    id: int
    initiator_trainer_id: int
    receiver_trainer_id: int
    initiator_pokemon_id: int
    receiver_pokemon_id: Optional[int]
    status: str
