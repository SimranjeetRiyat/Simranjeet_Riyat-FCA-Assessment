from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI
from fastapi import APIRouter, Request, HTTPException
import sqlite3
import sqlite3
from argon2 import PasswordHasher
from fastapi import HTTPException
from fastapi import Query

router = APIRouter()
app = FastAPI()

app.include_router(router)

@router.get("/rental_status")
def get_rental_status():
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT book_title,returned FROM fca_book_logs order by returned desc")
    results = cursor.fetchall()
    conn.close()

    if results:
        return {"rented_books": [row[0] for row in results if row[1] == 'FALSE'], "available_books": [row[0] for row in results if row[1] == 'TRUE']}
    else:
        return {"rented_books": []}

@router.get("/library_report")
def get_library_report():
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()
    cursor.execute("""
select book_title,book_id,user_id,user_email,borrowed_date,days_borrowed,days_overdue from fca_book_logs
where returned = 'FALSE'
    """)
    report = cursor.fetchall()
    conn.close()
    # return all the book data in a dictionary format
    if report:
        try:
            return {row[0]: {
                "book_id": row[1],
                "user_id": row[2],
                "user_email": row[3],
                "borrowed_date": row[4],
                "days_borrowed": row[5],
                "days_overdue": row[6]
            } for row in report}
        except IndexError:
            raise HTTPException(status_code=500, detail="Error processing report data")
