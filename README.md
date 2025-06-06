# 📘 FCA Library Management System

This is a FastAPI-based web application for managing library operations including login, book rentals, and wishlists. A SQLite database is used as the backend.

---

## Setup Instructions

1. **Install Dependencies:**

```
pip install -r requirements.txt
```

2. **Initialise Data And Restart Database (use only to run first time and then subsequently to delete data and retest):**

```
python initialisation/data_initialisation.py
```

This will create and populate the SQLite database.

3. **Run the Server:**

```
python main.py
```

4. **Access the App:**

Visit `http://localhost:8000` to access the login page.
Please enter any user id greater than 2 in the datasets/datasets_csv/library_members.csv to access the library user module and a user id of 1 or 2 to access the library_staff module 

---

## Unit Tests

Run tests using:

```
pytest -v unit_tests
```

---

## Endpoints Summary

| Endpoint                   | Method | Description                             | Payload Example                                      |
|----------------------------|--------|-----------------------------------------|------------------------------------------------------|
| `/login`                  | POST   | Authenticate a library member                     | `{"email": "alice.brown@fca_user.com", "password": "Maple$Stream91"}`               |
| `/books_availability`     | POST   | Check availability by title or author   | `{"book_names": ["Life of Pi","Fahrenheit 451"], "authors": ["Suzzane Collins"]}`   |
| `/wishlist?user_id=3`     | GET    | View wishlist for a user                | —                                                    |
| `/wishlist?user_id=3`     | POST   | Add books from wishlist                 | `{"book_titles": [The Hunger Games, Mockingjay]"action": "add"}`    |
| `/wishlist?user_id=3`     | POST   | Remove books from wishlist               | `{"book_titles": [Little Women], "action": "remove"}`    |
| `/login`                  | POST   | Authenticate a library staff member                     | `{"email": "jane.hargreave@fca_member.com", "password": "Moon.Rise63"}`               |
| `/rental_status`          | GET    | List available and borrowed books       | —                                                    |
| `/book_borrow?user_id=1`  | POST   | Borrow a book (requires staff user)     | `{"book_title": "Gone with the Wind", "user_email": "fred.hall@fca_user.com"}`        |
| `/book_return?user_id=1`  | POST   | Return a book and notify wishlist users | `{"book_title": "Angels & Demons"}`|
| `/library_report`         | GET    | Generate a current rental report        | —                                                    |

---