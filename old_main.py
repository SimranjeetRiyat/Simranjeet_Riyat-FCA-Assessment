import uvicorn
from fastapi import FastAPI
import sqlite3
import argon2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/login")
def read_root():
    return {"Hello There, Welcome to the FCA Library Management System! Please enter your email and password to log in."}

@app.post("/login")
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


@app.get("/books_availability")
def read_root():
    return {"Please enter the name of the author or the title of the book to check its availability."}

@app.post("/books_availability")
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

@app.get("/wishlist")
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

@app.post("/wishlist")
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

@app.get("/rental_status")
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

@app.get("/library_report")
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

@app.post("/book_borrow")
async def borrow_book(
    request: Request,
    user_id: int = Query(..., description="Library staff user ID")
):
    request_data = await request.json()
    book_title = request_data.get("book_title")
    user_email = request_data.get("user_email")
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()

    # Step 1: Validate that staff_user_id is a staff member
    cursor.execute("""
        SELECT 'TRUE' FROM fca_library_users
        WHERE id = ? AND staff_member = 'TRUE'
    """, (user_id,))
    if not cursor.fetchone():
        return {"error": "User is not authorized to borrow books."}

    # Step 2: Get the book_id from the title
    cursor.execute("SELECT id FROM fca_books WHERE title = ?", (book_title,))
    result = cursor.fetchone()
    if not result:
        return {"error": f"No book found with title '{book_title}'."}

    book_id = result[0]

    # Step 3: Update fca_book_status
    cursor.execute("""
        UPDATE fca_book_status
        SET borrowed = 'TRUE'
        WHERE book_id = ?
    """, (book_id,))

    # Step 4: Insert into fca_book_logs
    cursor.execute("""
        INSERT INTO fca_book_logs (book_id, book_title, user_id, user_email, borrowed_date, returned, date_returned, days_borrowed, overdue)
        VALUES (?, ?, ?, ?, DATE('now'), 'FALSE', NULL, 0, 'FALSE')
    """, (book_id, book_title, user_id, user_email))

    conn.commit()
    conn.close()

    return {"message": f"Book '{book_title}' borrowed successfully."}


@app.post("/book_return")
async def return_book(
    request: Request,
    user_id: int = Query(..., description="Library staff user ID")
):
    request_data = await request.json()
    book_title = request_data.get("book_title")
    conn = sqlite3.connect("datasets/SQLite_database/fca_library.db")
    cursor = conn.cursor()

    # Step 1: Validate that staff_user_id is a staff member
    cursor.execute("""
        SELECT 'TRUE' FROM fca_library_users
        WHERE id = ? AND staff_member = 'TRUE'
    """, (user_id,))
    if not cursor.fetchone():
        return {"error": "User is not authorized to return books."}

    # Step 2: Get the book_id from the title
    cursor.execute("SELECT id FROM fca_books WHERE title = ?", (book_title,))
    result = cursor.fetchone()
    if not result:
        return {"error": f"No book found with title '{book_title}'."}

    book_id = result[0]

    # Step 3: Update fca_book_status
    cursor.execute("""
        UPDATE fca_book_status
        SET borrowed = 'FALSE'
        WHERE book_id = ?
    """, (book_id,))

    # Step 4: Update fca_book_logs
    cursor.execute("""
        UPDATE fca_book_logs
        SET returned = 'TRUE',
            date_returned = DATE('now'),
            overdue = 'FALSE',
            days_overdue = 0
        WHERE book_id = ? AND returned = 'FALSE'
    """, (book_id,))

    # Step 5: Get emails and first names from wishlist
    cursor.execute("""
        SELECT u.email, u.first_name
        FROM fca_user_wishlist w
        JOIN fca_library_users u ON w.user_id = u.id
        WHERE w.book_id = ?
        order by w.date_added_to_wishlist desc           
    """, (book_id,))
    users_to_notify = cursor.fetchall()

    conn.commit()
    conn.close()

    # Step 6: Notify users with fake email including the email, subject matter, and body
    emails_to_notify = []
    for email, first_name in users_to_notify:
        emails_to_notify.append(email)
        print(f"""
        Email: {email}
        Subject: {book_title} is now available

        Dear {first_name},
        You are receiving this notification because you have expressed interest in the book {book_title}.
        The book has been returned and is now available for borrowing.

        Kind Regards,
        FCA Library Management System

        """
        )

    return {
        "message": f"Book '{book_title}' marked as returned.",
        "notified_users": emails_to_notify
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)


