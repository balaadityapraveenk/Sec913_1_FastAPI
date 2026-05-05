from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/products")
def get_products():
    return [
        {"name":"Laptop","price":70000},
        {"name":"Mobile","price":20000},
        {"name":"Projector","price":22222},
        {"name":"Tablet","price":30000}
    ]

@app.get("/welcome")
def get_products():
    return "Welcome to Sec-913"


class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "admin123":
        return{
            "UserStatus":1,
            "UserRole":1,
            "UserPendingTask":1
        }
    if data.username == "student" and data.password == "student123":
        return{
            "UserStatus":1,
            "UserRole":2,
            "UserPendingTask":5
        }
    if data.username == "staff" and data.password == "staff123":
        return{
            "UserStatus":1,
            "UserRole":3,
            "UserPendingTask":8
        }
    
    raise HTTPException(status_code=401, detail="Invalid username or password")
