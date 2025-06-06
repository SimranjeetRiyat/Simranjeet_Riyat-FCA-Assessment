CREATE TABLE IF NOT EXISTS fca_user_wishlist (
    id INTEGER  PRIMARY KEY,
    book_id INT NOT NULL,
    book_title VARCHAR(255) NULL,
    user_id INT NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    date_added_to_wishlist TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES fca_books(id),
    FOREIGN KEY (user_id) REFERENCES fca_library_users(id)
);

