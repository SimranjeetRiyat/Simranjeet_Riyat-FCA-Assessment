create table if not EXISTS fca_book_logs (
    id INTEGER PRIMARY KEY,
    book_id INT,
    book_title VARCHAR(255),
    user_id INT,
    user_email VARCHAR(255),
    borrowed_date DATE,
    returned BOOLEAN DEFAULT FALSE,
    date_returned DATE DEFAULT NULL,
    days_borrowed INT DEFAULT NULL,
    overdue BOOLEAN DEFAULT FALSE,
    days_overdue INT DEFAULT NULL,
    FOREIGN KEY (book_id) REFERENCES fca_books(id),
    FOREIGN KEY (user_id) REFERENCES fca_users(id)
);
