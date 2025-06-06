from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI
from fastapi import APIRouter, Request, HTTPException
import sqlite3
import sqlite3
from argon2 import PasswordHasher
from fastapi import HTTPException

router = APIRouter()

@router.get("/books_availability")
def read_root():
    return {"Please enter the name of the author or the title of the book to check its availability."}

@router.post("/books_availability")
async def data_entry(request: Request):
    search_data = await request.json()
    authors = search_data.get("authors")
    if isinstance(authors, list):
        authors = ', '.join([f"'{author.strip()}'" for author in authors])
    else:
        authors = f"'{authors.strip()}'" if authors else None

    book_name = search_data.get("book_names") 
    if isinstance(book_name, list):
        book_name = ', '.join([f"'{name.strip()}'" for name in book_name])
    else:
        book_name = f"'{book_name.strip()}'" if book_name else None
    
    if not authors and not book_name:
        raise HTTPException(status_code=400, detail="Please provide either authors or book_name to search.")
    
    with open("sql_commands/checking_book_availability.sql", "r") as f:
        sql_query = f.read()
        sql_query = sql_query.replace("/*__AUTHORS__*/", authors if authors else "NULL")
        sql_query = sql_query.replace("/*__BOOKS__*/", book_name if book_name else "NULL")
    
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()
    cursor.execute(sql_query,)

    results = cursor.fetchall()
    conn.close()

    print(results)
    available_books = []
    unavailable_books = []
    for row in results:
        if row[1] =='FALSE':
            available_books.append(row[0])
        else:
            unavailable_books.append(row[0])

    if results:
        return {"available_books": available_books, "unavailable_books": unavailable_books}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
