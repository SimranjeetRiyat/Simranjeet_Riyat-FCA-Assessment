SELECT id,first_name, last_name, password
FROM fca_library_users
WHERE email = ?;
-- This SQL command retrieves the first and last names of a user from the library_users table