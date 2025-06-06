CREATE TABLE IF NOT EXISTS fca_books (
    id int PRIMARY KEY,
    isbn VARCHAR(20),
    authors JSON,
    publication_year INT,
    title VARCHAR(255),
    language VARCHAR(50)
);

