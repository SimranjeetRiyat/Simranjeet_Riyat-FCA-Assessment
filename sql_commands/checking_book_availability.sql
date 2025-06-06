with book_authors as
(Select fca_books.id, fca_books.title, fca_books.authors,fca_book_status.borrowed
from fca_book_status
JOIN fca_books on fca_books.id = fca_book_status.book_id)

select title,borrowed from book_authors 
,json_each(book_authors.authors)
where
json_each.value in(/*__AUTHORS__*/)
-- json_each.value in('')
or
book_authors.title in (/*__BOOKS__*/)
order by book_authors.borrowed DESC;
