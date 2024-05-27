from fastapi import FastAPI
from app.api.endpoints import pokemon  # Adjust the import path based on your project structure
from app.api.endpoints import trainer  # Adjust the import path based on your project structure

app = FastAPI(title='Pokemon Project', version='1.0', description='A FastAPI application to manage Pokémon data')

# this is our pokemon router, 
# responsible for any Pokemon related crud operations.
app.include_router(pokemon.router, prefix='/api/v1/pokemon', tags=['pokemon'])
app.include_router(trainer.router, prefix='/api/v1/trainer', tags=['trainer'])

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Pokémon API!"}
