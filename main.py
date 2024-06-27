import logging
from fastapi import FastAPI
from app.api.endpoints import pokemon, trainer, trade

logging.basicConfig(level=logging.INFO)

app = FastAPI(title='Pokemon Project', version='1.0', description='A FastAPI application to manage Pokémon data')

# Include routers
app.include_router(pokemon.router, prefix='/api/v1/pokemon', tags=['pokemon'])
app.include_router(trainer.router, prefix='/api/v1/trainer', tags=['trainer'])
app.include_router(trade.router, prefix='/api/v1/trade', tags=['trade'])

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Pokémon API!"}
