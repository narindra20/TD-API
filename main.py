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
    
    
    
#EXO3
class Task(BaseModel):
    id: int
    title: str
    completed: bool

tasks_db = [
    Task(id=1, title="Faire les courses", completed=False),
    Task(id=2, title="Étudier FastAPI", completed=True),
]


@app.get("/tasks", response_model=List[Task], summary="Retourne une liste de tâches")
def get_tasks():
    return tasks_db


@app.post("/tasks", response_model=List[Task], status_code=201, summary="Crée une liste de nouvelles tâches")
def create_tasks(new_tasks: List[Task]):
    tasks_db.extend(new_tasks)
    return new_tasks


@app.get("/tasks/{id}", response_model=Task, summary="Retourne une tâche par son ID")
def get_task_by_id(id: int):
    for task in tasks_db:
        if task.id == id:
            return task
    return {"message": "Task not found"}, 404


@app.delete("/tasks/{id}", response_model=Task, summary="Supprime une tâche par son ID")
def delete_task_by_id(id: int):
    for task in tasks_db:
        if task.id == id:
            tasks_db.remove(task)
            return task
    return {"message": "Task not found"}, 404


@app.delete("/tasks", response_model=List[Task], summary="Supprime une liste de tâches par leurs identifiants")
def delete_tasks_by_ids(ids: List[int]):
    deleted = []
    for task in tasks_db[:]:  
        if task.id in ids:
            tasks_db.remove(task)
            deleted.append(task)
    return deleted

