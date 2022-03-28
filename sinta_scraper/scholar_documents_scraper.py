from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get
from string_utils.validation import is_integer

import utils
from utils.config import get_config


def author_scholar_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                        min_year=None, max_year=None, max_workers=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentsgs'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = utils.cast(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(worker, author_id, page, worker_result)

    if min_year is not None:
        worker_result = [doc for doc in worker_result if is_integer(str(doc['year'])) and doc['year'] >= min_year]

    if max_year is not None:
        worker_result = [doc for doc in worker_result if is_integer(str(doc['year'])) and doc['year'] <= max_year]

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=documentsgs'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data = parse(soup)

    worker_result.extend(data)


def parse(soup):
    rows = soup.select('table.uk-table tr')
    result = []

    for row in rows:
        link = row.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        info = row.select('dd.indexed-by')[0].text.strip().split('|')
        citations = row.select('.index-val')[1].text.strip()

        result.append({
            'title': link.text,
            'url': link['href'],
            'publisher': info[0].strip(),
            'year': utils.cast(info[3].strip()),
            'citations': utils.cast(citations) if is_integer(citations) else 0
        })

    return result
