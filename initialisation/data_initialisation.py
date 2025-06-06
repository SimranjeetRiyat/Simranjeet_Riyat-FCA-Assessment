# run_both.py
import subprocess
from initialisation.upload_csv_into_database import FCADataInserter

# delete file if it exists
import os

db_path = "datasets/SQLite_database/fca_library.db"
if os.path.exists(db_path):
	os.remove(db_path)
subprocess.run(["python", "db_cleaning/create_books_db.py"])
inserter = FCADataInserter()
inserter.insert_books()
inserter.insert_library_members()
inserter.insert_book_status()
inserter.insert_book_logs()
inserter.insert_user_wishlist()
