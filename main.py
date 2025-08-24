from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from typing import List
from pydantic import BaseModel

app = FastAPI(
    title="API Ping",
    version="1.0.0",
    description='Une API qui répond "pong" à un ping.'
)

#EXO1
@app.get("/ping", response_class=PlainTextResponse, summary="Vérifie la disponibilité du service")
def ping():
    return "pong"

#EXO2
class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users", response_model=List[User], summary="Récupère une liste paginée d'utilisateurs")
def get_users(
    page: int = Query(1, ge=1, description="Numéro de la page"),
    size: int = Query(20, ge=1, description="Nombre d'utilisateurs par page")
):
    try:
        all_users = [
            {
                "id": 1, 
                "name": "Alice", 
                "email": "alice@example.com"
            },
            
            {
                "id": 2, 
                "name": "Bob", 
                "email": "bob@example.com"
            },
            
            {
                "id": 3, 
                "name": "Charlie", 
                "email": "charlie@example.com"
            },
            
            {
                "id": 4, 
                "name": "Diana", 
                "email": "diana@example.com"
            },
            
            {
                "id": 5, 
                "name": "Eve", 
                "email": "eve@example.com"
            },
        ]
        
        start = (page - 1) * size
        end = start + size
        return all_users[start:end]
    except Exception:
        return {"error": "Bad types for provided query parameters"}
