import sqlite3

def create_all_tables(db_name, sql_paths):
    conn = sqlite3.connect(f"datasets/SQLite_database/{db_name}")
    cursor = conn.cursor()

    for sql_path in sql_paths:
        with open(sql_path, "r") as f:
            sql_script = f.read()
            cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print(f"Database {db_name} created successfully with all tables.")

if __name__ == "__main__":
    sql_files = [
        "sql_commands/creating_tables/create_books.sql",
        "sql_commands/creating_tables/create_user_data.sql",
        "sql_commands/creating_tables/create_book_status.sql",
        "sql_commands/creating_tables/create_book_logs.sql",
        "sql_commands/creating_tables/create_user_wishlist.sql",        
    ]
    create_all_tables("fca_library.db", sql_files)


