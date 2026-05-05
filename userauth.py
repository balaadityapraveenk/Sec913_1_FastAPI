#file name :userauth.py
# pip install fastapi uvicorn pydantic sqlalchemy psycopg2
# uvicorn userauth:app --reload
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# ================= DATABASE =================
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/TaskHub1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ================= MODEL =================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(Integer)
    pending_task = Column(Integer)

# Create table
Base.metadata.create_all(bind=engine)

# ================= FASTAPI =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= REQUEST MODEL =================
class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: int
    pending_task: int
# ================= ROUTES =================

@app.get("/products")
def get_products():
    return [
        {"name": "Laptop", "price": 7000000},
        {"name": "Mobile", "price": 20000},
        {"name": "Projector", "price": 22222},
        {"name": "Tablet", "price": 30000}
    ]

@app.get("/welcome")
def welcome():
    return "Welcome to Sec913 New"

# ================= LOGIN (DB CONNECTED) =================
@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    
    user = db.query(User).filter(
        User.username == data.username,
        User.password == data.password
    ).first()
    
    db.close()

    if user:
        return {
            "UserStatus": 1,
            "UserRole": user.role,
            "UserPendingTask": user.pending_task
        }
    else:
        return {"UserStatus":0}

    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/add_user")
def add_user(user: UserCreate):
    db = SessionLocal()

    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create new user
    new_user = User(
        username=user.username,
        password=user.password,
        role=user.role,
        pending_task=user.pending_task
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "message": "User added successfully",
        "user_id": new_user.id
    }

    # Database :TaskHub
#     CREATE TABLE users (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR(50) UNIQUE,
#     password VARCHAR(50),
#     role INT,
#     pending_task INT
# );

# INSERT INTO users (username, password, role, pending_task) VALUES
# ('admin', 'admin123', 1, 1),
# ('student', 'student123', 2, 5),
# ('staff', 'staff123', 3, 8);