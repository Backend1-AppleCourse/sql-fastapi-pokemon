from fastapi import FastAPI
from app.api import pokemon, trainer, trade

app = FastAPI()

app.include_router(pokemon.router, prefix="/api/v1/pokemons")
app.include_router(trainer.router, prefix="/api/v1")
app.include_router(trade.router, prefix='/api/v1/trade', tags=['trade'])

@app.get("/health")
def health():
    return {"status": "ok"}
