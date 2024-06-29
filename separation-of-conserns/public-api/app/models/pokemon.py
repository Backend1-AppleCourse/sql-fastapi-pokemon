from pydantic import BaseModel
from typing import List

class PokemonCreate(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
