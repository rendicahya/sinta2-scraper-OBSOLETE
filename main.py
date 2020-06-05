from scraper import *

for dept_id in [55201, 57201, 59201, 83207, 56201, 55101]:
    author_ids = get_dept_authors(dept_id)

    for author_id in author_ids:
        author = get_author(author_id)

        print(author)
