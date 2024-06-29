# pokemon.py
from pydantic import BaseModel
from typing import List

class PokemonBase(BaseModel):
    id: int
    name: str
    height: float
    weight: float
    types: List[str]

class PokemonCreate(PokemonBase):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    
class Pokemon(PokemonBase):
    class Config:
        orm_mode = True
        
