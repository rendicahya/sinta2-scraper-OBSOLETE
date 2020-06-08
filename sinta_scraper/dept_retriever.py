import re
import threading

from bs4 import BeautifulSoup
from requests import get

import utils


def dept_authors_worker(affil_id, dept_id, page, all_authors):
    page_url = f'http://sinta.ristekbrin.go.id/departments/detail?page={page}&afil={affil_id}&id={dept_id}&view=authors&sort=year2'
    page_html = get(page_url)
    page_soup = BeautifulSoup(page_html.content, 'html.parser')
    links = page_soup.select('.uk-description-list-line .text-blue')
    authors = []

    for i in range(len(links)):
        link = links[i]
        author_id = re.search(r'id=(\d+)', link['href']).group(1)
        author_name = link.text

        authors.append({
            'id': author_id,
            'name': author_name.title()
        })

    all_authors.extend(authors)


def dept_authors(affil_id, dept_id, output_format='dictionary', pretty_print=None):
    url = f'http://sinta.ristekbrin.go.id/departments/detail?afil={affil_id}&id={dept_id}&view=authors'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = int(page_info[0].text.strip().split()[3])
    threads = []
    authors = []

    for page in range(1, n_page + 1):
        thread = threading.Thread(target=dept_authors_worker, args=(affil_id, dept_id, page, authors))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(authors, output_format=output_format, pretty_print=pretty_print)
