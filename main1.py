# File Name: main1.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# ================= DATABASE =================

DATABASE_URL = "postgresql+psycopg2://postgres:admin123@127.0.0.1:5432/studentportal"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ================= MODEL =================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    mobile = Column(String(20))
    email = Column(String(100), unique=True)
    password = Column(String(100))

# Create table automatically
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

# ================= REQUEST MODELS =================

class SignupRequest(BaseModel):
    fullname: str
    mobile: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ================= HOME API =================

@app.get("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }


# ================= SIGNUP API =================

@app.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        db.close()
        return {
            "message": "Email already registered"
        }

    # Create new user
    new_user = User(
        fullname=data.fullname,
        mobile=data.mobile,
        email=data.email,
        password=data.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "Signup successful"
    }


# ================= LOGIN API =================

@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password
    ).first()

    db.close()

    if user:
        return {
            "message": "Login successful"
        }

    return {
        "message": "Invalid email or password"
    }