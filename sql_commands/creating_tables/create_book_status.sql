CREATE TABLE IF NOT EXISTS fca_book_status (
    book_id INTEGER PRIMARY KEY,
    book_title VARCHAR(255),
    borrowed BOOLEAN NOT NULL,
    FOREIGN KEY (book_id) REFERENCES fca_books(id)
);

