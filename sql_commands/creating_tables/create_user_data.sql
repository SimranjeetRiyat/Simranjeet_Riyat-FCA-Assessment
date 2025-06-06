CREATE TABLE IF NOT EXISTS fca_library_users (
    id INTEGER  PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    staff_member BOOLEAN DEFAULT FALSE
);
   