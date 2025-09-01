from fastapi import FastAPI, Query, Path, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
import uuid

app = FastAPI()

security = HTTPBasic()

#EXO1 – Ping 
@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"

#EXO2 – Utilisateurs 
class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users", response_model=List[User])
def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1)
):
    all_users = [
        User(id=1, name="Alice", email="alice@example.com"),
        User(id=2, name="Bob", email="bob@example.com"),
        User(id=3, name="Charlie", email="charlie@example.com"),
        User(id=4, name="Diana", email="diana@example.com"),
        User(id=5, name="Eve", email="eve@example.com"),
    ]
    start = (page - 1) * size
    end = start + size
    return all_users[start:end]

#EXO3 – Tâches 
class Task(BaseModel):
    id: int
    title: str
    completed: bool

tasks_db = [
    Task(id=1, title="Faire les courses", completed=False),
    Task(id=2, title="Étudier FastAPI", completed=True),
]

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=List[Task], status_code=201)
def create_tasks(new_tasks: List[Task]):
    tasks_db.extend(new_tasks)
    return new_tasks

@app.get("/tasks/{id}", response_model=Task)
def get_task_by_id(id: int):
    for task in tasks_db:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", response_model=Task)
def delete_task_by_id(id: int):
    for task in tasks_db:
        if task.id == id:
            tasks_db.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks", response_model=List[Task])
def delete_tasks_by_ids(ids: List[int]):
    deleted = []
    for task in tasks_db[:]:
        if task.id in ids:
            tasks_db.remove(task)
            deleted.append(task)
    return deleted

#EXO4 – Produits
class Product(BaseModel):
    name: str
    expiration_datetime: datetime
    price: float

products_db = [
    Product(name="Lait entier", expiration_datetime=datetime(2025, 9, 1, 12, 0), price=2.49),
    Product(name="Pain complet", expiration_datetime=datetime(2025, 8, 28, 8, 30), price=1.99),
    Product(name="Yaourt nature", expiration_datetime=datetime(2025, 9, 3, 10, 0), price=0.99),
]

@app.get("/products", response_model=List[Product])
def get_products(
    limit: Optional[int] = Query(None, ge=1),
    q: Optional[str] = Query(None)
):
    results = products_db
    if q:
        results = [p for p in results if q.lower() in p.name.lower()]
    if limit:
        results = results[:limit]
    return results

# ---------------- EXO5 – Commandes ----------------
class Order(BaseModel):
    identifier: int
    customer_name: str
    creation_datetime: datetime
    total_amount: float

orders_db = [
    Order(identifier=101, customer_name="Narindra", creation_datetime=datetime(2025, 8, 26, 10, 0), total_amount=12.99),
    Order(identifier=102, customer_name="Alice", creation_datetime=datetime(2025, 8, 26, 11, 30), total_amount=7.50),
]

@app.get("/orders", response_model=List[Order])
def get_orders(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    start = (page - 1) * size
    end = start + size
    return orders_db[start:end]

@app.post("/orders", response_model=Order)
def create_order(
    order: Order,
    credentials: HTTPBasicCredentials = Depends(security)
):
    if credentials.username != "admin" or credentials.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )
    orders_db.append(order)
    return order

#EXO6 – Profils utilisateurs 
class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    birthdate: date
    email: EmailStr

class Address(BaseModel):
    address_street: str
    address_city: str
    address_country: str
    address_postal_code: str

class Preferences(BaseModel):
    needs_newsletter: bool
    language: str = Field(..., enum=["mg", "fr", "eng"])

class CreateUserProfile(BaseModel):
    personal_info: PersonalInfo
    address: Address
    preferences: Preferences

class UserProfile(BaseModel):
    identifier: str
    personal_info: PersonalInfo
    address: Address
    preferences: Preferences

users_db: List[UserProfile] = []

@app.post("/profiles", response_model=List[UserProfile])
def create_profiles(profiles: List[CreateUserProfile]):
    created = []
    for profile in profiles:
        user = UserProfile(
            identifier=str(uuid.uuid4()),
            personal_info=profile.personal_info,
            address=profile.address,
            preferences=profile.preferences
        )
        users_db.append(user)
        created.append(user)
    return created

@app.get("/profiles/{id}", response_model=UserProfile)
def get_profile(id: str = Path(...)):
    for user in users_db:
        if user.identifier == id:
            return user
    raise HTTPException(status_code=404, detail="Profil non trouvé")

@app.put("/profiles/{id}/personalInfo", response_model=UserProfile)
def update_profile_info(id: str, info: PersonalInfo):
    for user in users_db:
        if user.identifier == id:
            user.personal_info = info
            return user
    raise HTTPException(status_code=404, detail="Profil non trouvé")

@app.put("/profiles/{id}/address", response_model=UserProfile)
def update_profile_address(id: str, address: Address):
    for user in users_db:
        if user.identifier == id:
            user.address = address
            return user
    raise HTTPException(status_code=404, detail="Profil non trouvé")

@app.put("/profiles/{id}/preferences", response_model=UserProfile)
def update_profile_preferences(id: str, prefs: Preferences):
    for user in users_db:
        if user.identifier == id:
            user.preferences = prefs
            return user
    raise HTTPException(status_code=404, detail="Profil non trouvé")
