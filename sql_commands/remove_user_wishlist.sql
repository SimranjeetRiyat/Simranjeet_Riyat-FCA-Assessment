DELETE FROM fca_user_wishlist
WHERE user_id = ?
    AND book_id IN (
        SELECT b.id
        FROM fca_books b
        WHERE b.title IN (/*__BOOKS__*/)
    );
