import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

from utils.config import get_config
from utils.utils import format_output, cast, listify


def retrieve_authors(dept_id, affil_id, output_format='dictionary'):
    domain = get_config()['domain']
    url = f'{domain}/departments/detail?afil={affil_id}&id={dept_id}&view=authors'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = cast(page_info[0].text.strip().split()[3])
    worker_result = author_parser(soup)

    with ThreadPoolExecutor() as executor:
        for page in range(2, n_page + 1):
            executor.submit(retrieve_authors_worker, dept_id, affil_id, page, worker_result)

    return format_output(worker_result, output_format)


def retrieve_authors_worker(dept_id, affil_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/departments/detail?page={page}&afil={affil_id}&id={dept_id}&view=authors&sort=year2'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data = author_parser(soup)

    worker_result.extend(data)


def author_parser(soup):
    links = soup.select('.uk-description-list-line .text-blue')
    result = []

    for i in range(len(links)):
        link = links[i]
        author_id = re.search(r'id=(\d+)', link['href']).group(1)
        author_name = link.text

        result.append({
            'id': author_id,
            'name': author_name.title()
        })

    return result


def dept_authors(dept_ids, affil_id, output_format='dictionary'):
    dept_ids = listify(dept_ids)
    worker_result = []

    with ThreadPoolExecutor() as executor:
        for dept_id in dept_ids:
            executor.submit(dept_authors_worker, dept_id, affil_id, worker_result)

    return format_output(worker_result, output_format)


def dept_authors_worker(dept_id, affil_id, worker_result):
    authors = retrieve_authors(dept_id, affil_id)

    worker_result.extend(authors)
