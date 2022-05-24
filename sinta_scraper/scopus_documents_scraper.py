import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get
from string_utils.validation import is_integer

import utils
from sinta_scraper.dept_scraper import dept_authors
from utils.config import get_config


def author_scopus_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                       min_date=None, max_date=None, max_workers=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentsscopus'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = utils.cast(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)
    date_format = '%Y-%m-%d'

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(worker, author_id, page, worker_result)

    if min_date is not None:
        min_date_parsed = datetime.strptime(min_date, date_format)
        worker_result = [doc for doc in worker_result if datetime.strptime(doc['date'], date_format) >= min_date_parsed]

    if max_date is not None:
        max_date_parsed = datetime.strptime(max_date, date_format)
        worker_result = [doc for doc in worker_result if datetime.strptime(doc['date'], date_format) <= max_date_parsed]

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def author_scopus_journal_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                               min_date=None, max_date=None, max_workers=None):
    docs = author_scopus_docs(author_id, min_date=min_date, max_date=max_date, max_workers=max_workers)
    journal_docs = [doc for doc in docs if doc['type'] == 'Journal']

    return utils.format_output(journal_docs, output_format, pretty_print, xml_library)


def author_scopus_conference_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                                  min_date=None, max_date=None, max_workers=None):
    docs = author_scopus_docs(author_id, min_date=min_date, max_date=max_date, max_workers=max_workers)
    journal_docs = [doc for doc in docs if doc['type'].startswith('Conference')]

    return utils.format_output(journal_docs, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=documentsscopus'
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
        info1 = row.select('.index-val')
        quartile = info1[0].text.strip()
        citations = info1[1].text.strip()
        info2 = row.select('dd.indexed-by')[0].text.strip().split('|')

        result.append({
            'title': link.text,
            'url': link['href'],
            'publisher': info2[0].strip(),
            'date': info2[3].strip(),
            'type': info2[4].strip(),
            'quartile': utils.cast(quartile[1]) if re.search(r'^Q[1-4]{1}$', quartile) else '-',
            'citations': utils.cast(citations) if is_integer(citations) else 0
        })

    return result


def dept_scopus_docs(dept_ids, affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                     max_workers=None):
    if type(dept_ids) is not list and type(dept_ids) is not tuple:
        dept_ids = [dept_ids]

    authors = []
    worker_result = []

    for dept_id in dept_ids:
        authors.extend(dept_authors(dept_id, affil_id))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for author in authors:
            executor.submit(dept_scopus_docs_worker, author['id'], worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def dept_scopus_docs_worker(author_id, worker_result):
    researches = author_scopus_docs(author_id)

    worker_result.extend(researches)
