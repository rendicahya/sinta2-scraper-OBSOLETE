import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get
from string_utils.validation import is_integer

from sinta_scraper.dept_scraper import dept_authors
from utils.config import get_config
from utils.utils import cast, format_output, listify


def author_scopus(author_id, output_format='dictionary', min_date=None, max_date=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentsscopus'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = cast(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)
    date_format = '%Y-%m-%d'

    with ThreadPoolExecutor() as executor:
        for page in range(2, n_page + 1):
            executor.submit(worker, author_id, page, worker_result)

    if min_date is not None:
        min_date_parsed = datetime.strptime(min_date, date_format)
        worker_result = [doc for doc in worker_result if datetime.strptime(doc['date'], date_format) >= min_date_parsed]

    if max_date is not None:
        max_date_parsed = datetime.strptime(max_date, date_format)
        worker_result = [doc for doc in worker_result if datetime.strptime(doc['date'], date_format) <= max_date_parsed]

    return format_output(worker_result, output_format)


def author_scopus_journal(author_id, output_format='dictionary', min_date=None, max_date=None):
    docs = author_scopus(author_id, min_date=min_date, max_date=max_date)
    journal_docs = [doc for doc in docs if doc['type'] == 'Journal']

    return format_output(journal_docs, output_format)


def author_scopus_conference(author_id, output_format='dictionary', min_date=None, max_date=None):
    docs = author_scopus(author_id, min_date=min_date, max_date=max_date)
    journal_docs = [doc for doc in docs if doc['type'].startswith('Conference')]

    return format_output(journal_docs, output_format)


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
            'quartile': cast(quartile[1]) if re.search(r'^Q[1-4]{1}$', quartile) else '-',
            'citations': cast(citations) if is_integer(citations) else 0
        })

    return result


def dept_scopus(dept_ids, affil_id, output_format='dictionary', max_workers=None):
    dept_ids = listify(dept_ids)

    authors = []
    worker_result = []

    for dept_id in dept_ids:
        authors.extend(dept_authors(dept_id, affil_id))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for author in authors:
            executor.submit(dept_scopus_docs_worker, author['id'], worker_result)

    return format_output(worker_result, output_format)


def dept_scopus_docs_worker(author_id, worker_result):
    researches = author_scopus(author_id)

    worker_result.extend(researches)
