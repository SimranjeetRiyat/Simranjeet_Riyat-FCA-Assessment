INSERT INTO fca_user_wishlist (book_id, book_title, user_id, user_email, date_added_to_wishlist)
SELECT b.id, b.title, u.id, u.email, DATE('now')
FROM fca_books b
JOIN fca_book_status s ON b.id = s.book_id
JOIN fca_library_users u ON u.id = ?
WHERE b.title IN (/*__BOOKS__*/)
  AND s.borrowed = 'TRUE'
  AND u.staff_member = 'FALSE'

  AND NOT EXISTS (
    SELECT 1
    FROM fca_user_wishlist uw
    WHERE uw.user_id = u.id
      AND uw.book_id = b.id
);

