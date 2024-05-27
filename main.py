from fastapi import FastAPI
from app.api.endpoints import pokemon  # Adjust the import path based on your project structure

app = FastAPI(title='Pokemon Project', version='1.0', description='A FastAPI application to manage Pokémon data')

# Include the routers
app.include_router(pokemon.router, prefix='/api/v1/pokemon', tags=['pokemon'])

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Pokémon API!"}
