from pydantic import BaseModel

class TrainerPokemonRequest(BaseModel):
    trainer_name: str
    pokemon_name: str

class TrainerPokemonResponse(BaseModel):
    message: str
    trainer_name: str
    pokemon_name: str
