import csv
import sqlite3
import re
import json
import argon2

class FCADataInserter:
    def __init__(self, db_path="datasets/SQLite_database/fca_library.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        return conn, cursor

    def insert_books(self, csv_path="datasets/datasets_csv/Backend Data - Backend Data.csv"):
        conn, cursor = self._get_connection()
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "," in row["Authors"]:
                    row["Authors"] = [re.sub(r'\s+', ' ', name.strip()) for name in row["Authors"].split(',')]
                else:
                    row["Authors"] = [re.sub(r'\s+', ' ', row["Authors"].strip())]
                row["Authors"] = json.dumps(row["Authors"])
                cursor.execute(
                    """
                    INSERT INTO fca_books (id,isbn,authors,publication_year,title,language) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (row["Id"], row["ISBN"], row["Authors"], row["Publication Year"], row["Title"], row["Language"])
                )
        conn.commit()
        conn.close()

    def insert_library_members(self, csv_path="datasets/datasets_csv/library_members.csv"):
        conn, cursor = self._get_connection()
        hasher = argon2.PasswordHasher()
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["password"] = hasher.hash(row["password"])
                cursor.execute(
                    """
                    INSERT INTO fca_library_users (id,email,password,first_name,last_name,staff_member) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (row["id"], row["email"], row["password"], row["first_name"], row["last_name"],row["staff_member"])
                )
        conn.commit()
        conn.close()

    def insert_book_status(self, csv_path="datasets/datasets_csv/book_status.csv"):
        conn, cursor = self._get_connection()
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO fca_book_status (book_id,book_title,borrowed) VALUES (?, ?, ?)
                    """,
                    (row["book_id"], row["book_title"], row["borrowed"])
                )
        conn.commit()
        conn.close()

    def insert_book_logs(self, csv_path="datasets/datasets_csv/book_logs.csv"):
        conn, cursor = self._get_connection()
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO fca_book_logs (id,book_id,book_title,user_id,user_email,borrowed_date,returned,date_returned,days_borrowed,overdue,days_overdue) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (row["id"], row["book_id"], row["book_title"], row["user_id"], row["user_email"], row["borrowed_date"], row["returned"], row["date_returned"],row["days_borrowed"], row["overdue"], row["days_overdue"])
                )
        conn.commit()
        conn.close()

    def insert_user_wishlist(self, csv_path="datasets/datasets_csv/user_wishlist.csv"):
        conn, cursor = self._get_connection()
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO fca_user_wishlist (id,book_id,book_title,user_id,user_email,date_added_to_wishlist) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (row["id"], row["book_id"], row["book_title"], row["user_id"], row["user_email"], row["date_added_to_wishlist"])
                )
        conn.commit()
        conn.close()

if __name__ == "__main__":
    inserter = FCADataInserter()
    inserter.insert_books()
    inserter.insert_library_members()
    inserter.insert_book_status()
    inserter.insert_book_logs()
    inserter.insert_user_wishlist()
    print("All data inserted successfully.")