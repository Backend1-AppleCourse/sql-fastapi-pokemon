# pokemon.py
from pydantic import BaseModel

class Pokemon(BaseModel):
    name: str
    type: str

    class Config:
        orm_mode = True
