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
    pass

class Pokemon(PokemonBase):
    class Config:
        orm_mode = True
        
