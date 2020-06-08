import re
import threading

from bs4 import BeautifulSoup
from requests import get

import utils


def dept_authors(dept_id, affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    url = f'http://sinta.ristekbrin.go.id/departments/detail?afil={affil_id}&id={dept_id}&view=authors'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = int(page_info[0].text.strip().split()[3])
    threads = []
    worker_result = []

    for page in range(1, n_page + 1):
        thread = threading.Thread(target=dept_authors_worker, args=(dept_id, affil_id, page, worker_result))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def dept_authors_worker(dept_id, affil_id, page, worker_result):
    page_url = f'http://sinta.ristekbrin.go.id/departments/detail?page={page}&afil={affil_id}&id={dept_id}&view=authors&sort=year2'
    page_html = get(page_url)
    page_soup = BeautifulSoup(page_html.content, 'html.parser')
    links = page_soup.select('.uk-description-list-line .text-blue')

    for i in range(len(links)):
        link = links[i]
        author_id = re.search(r'id=(\d+)', link['href']).group(1)
        author_name = link.text

        worker_result.append({
            'id': author_id,
            'name': author_name.title()
        })


def depts_authors(dept_ids, affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    worker_result = []
    threads = []

    for dept_id in dept_ids:
        thread = threading.Thread(target=depts_authors_worker, args=(dept_id, affil_id, worker_result))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def depts_authors_worker(dept_id, affil_id, worker_result):
    authors = dept_authors(dept_id, affil_id)

    worker_result.extend(authors)
