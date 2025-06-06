from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI
from fastapi import APIRouter, Request, HTTPException
import sqlite3
import sqlite3
from argon2 import PasswordHasher
from fastapi import HTTPException

router = APIRouter()

@router.get("/login")
def read_root():
    return {"Hello There, Welcome to the FCA Library Management System! Please enter your email and password to log in."}

@router.post("/login")
async def data_entry(request: Request):
    login_data = await request.json()
    email = login_data.get("email")
    password = login_data.get("password")
    with open("sql_commands/username_password.sql", "r") as f:
        sql_query = f.read()
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()
    cursor.execute(sql_query, (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user_id, first_name, last_name, hashed_pw = row
        try:
            if PasswordHasher().verify(hashed_pw, password):
                return {"message": f"Login successful, welcome {first_name} {last_name}!", "user_id": user_id}
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        except VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Incorrect password")

    else:
        raise HTTPException(status_code=404, detail="User not found")

