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
