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

@router.get("/wishlist")
def get_wishlist(user_id: int = Query(..., description="User ID")):
    # Fetch wishlist items for the user from the database
    
    sql_query = """
        SELECT book_title FROM fca_book_status 
        WHERE book_id IN (
            SELECT book_id FROM fca_user_wishlist WHERE user_id = ?
        )
    """
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()
    cursor.execute(sql_query, (user_id,))
    wishlist_items = cursor.fetchall()
    conn.close()

    if wishlist_items:
        return {"wishlist": [item[0] for item in wishlist_items]}
    else:
        return {"wishlist": []}

@router.post("/wishlist")
async def add_to_wishlist(request: Request, user_id: int = Query(..., description="User ID")):
    data = await request.json()

    book_titles = data.get("book_titles")
    if isinstance(book_titles, list):
        book_titles = ', '.join([f"'{name.strip()}'" for name in book_titles])
    else:
        book_titles = f"'{book_titles.strip()}'" if book_titles else None
    print(book_titles)

    if not book_titles:
        raise HTTPException(status_code=400, detail="Book title is required")
    
    if data.get("action")=="add":
        sql_file = "sql_commands/insert_user_wishlist.sql"
    elif data.get("action")=="remove":
        sql_file = "sql_commands/remove_user_wishlist.sql"

    with open(sql_file, "r") as f:
        sql_query = f.read()
    sql_query = sql_query.replace("/*__BOOKS__*/", book_titles)
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()
    print(sql_query)
    cursor.execute(sql_query,(user_id,))
    # see the final query
    conn.commit()
    conn.close()
    return get_wishlist(user_id=user_id)



