from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils
from sinta_scraper.dept_scraper import dept_authors
from utils.config import get_config


def author_ipr(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml', max_workers=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=ipr'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = utils.cast(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(worker, author_id, page, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=ipr'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data = parse(soup)

    worker_result.extend(data)


def parse(soup):
    rows = soup.select('table.uk-table tr')
    result = []

    for row in rows:
        h4 = row.select('h4.uk-text-primary')

        if not h4:
            continue

        h4 = h4[0]
        info = row.select('.uk-text-success')

        result.append({
            'id': info[0].text.strip(),
            'title': h4.text.strip(),
            'category': info[1].text.strip(),
            'year': info[2].text.strip(),
            'holder': info[3].text.strip()
        })

    return result


def dept_ipr(dept_ids, affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
             max_workers=None):
    if type(dept_ids) is not list and type(dept_ids) is not tuple:
        dept_ids = [dept_ids]

    authors = []
    worker_result = []

    for dept_id in dept_ids:
        authors.extend(dept_authors(dept_id, affil_id))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for author in authors:
            executor.submit(dept_ipr_worker, author['id'], worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def dept_ipr_worker(author_id, worker_result):
    researches = author_ipr(author_id)

    worker_result.extend(researches)
