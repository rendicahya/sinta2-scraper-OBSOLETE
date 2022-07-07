import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get
from string_utils.validation import is_integer

from utils.config import get_config
from utils.utils import cast, format_output, listify


def author_scopus(author_id, output_format='dictionary', min_date=None, max_date=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentsscopus'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = cast(page_info[0].text.strip().split()[3])
    worker_result = scopus_parser(soup, min_date, max_date)

    with ThreadPoolExecutor() as executor:
        for page in range(2, n_page + 1):
            executor.submit(author_scopus_worker, author_id, page, min_date, max_date, worker_result)

    return format_output(worker_result, output_format)


def author_scopus_journal(author_id, output_format='dictionary', min_date=None, max_date=None):
    docs = author_scopus(author_id, min_date=min_date, max_date=max_date)
    journal_docs = [doc for doc in docs if doc['type'] == 'Journal']

    return format_output(journal_docs, output_format)


def author_scopus_conference(author_id, output_format='dictionary', min_date=None, max_date=None):
    docs = author_scopus(author_id, min_date=min_date, max_date=max_date)
    journal_docs = [doc for doc in docs if doc['type'].startswith('Conference')]

    return format_output(journal_docs, output_format)


def author_scopus_worker(author_id, page, min_date, max_date, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=documentsscopus'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data = scopus_parser(soup, min_date, max_date)

    worker_result.extend(data)


def dept_scopus(dept_ids, affil_id, output_format='dictionary', min_date=None, max_date=None):
    dept_ids = listify(dept_ids)
    worker_result = []
    domain = get_config()['domain']

    for dept_id in dept_ids:
        url = f'{domain}/departments/detail?afil={affil_id}&id={dept_id}&view=documentsscopus'
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        page_info = soup.select('.uk-width-large-1-2.table-footer')
        n_page = cast(page_info[0].text.strip().split()[3])

        worker_result.extend(scopus_parser(soup, min_date, max_date))

        with ThreadPoolExecutor() as executor:
            for page in range(2, n_page + 1):
                executor.submit(dept_scopus_docs_worker, dept_id, affil_id, page, min_date, max_date,
                                worker_result)

    return format_output(worker_result, output_format)


def dept_scopus_docs_worker(dept_id, affil_id, page, min_date, max_date, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/departments/detail?page={page}&id={dept_id}&afil={affil_id}&view=documentsscopus'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    result = scopus_parser(soup, min_date, max_date)

    worker_result.extend(result)


def scopus_parser(soup, min_date, max_date):
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
        date = info2[3].strip()
        date_format = '%Y-%m-%d'
        date_parsed = datetime.strptime(date, date_format)

        if min_date is not None:
            min_date_parsed = datetime.strptime(min_date, date_format)

            if date_parsed < min_date_parsed:
                continue

        if max_date is not None:
            max_date_parsed = datetime.strptime(max_date, date_format)

            if date_parsed > max_date_parsed:
                continue

        result.append({
            'title': link.text,
            'url': link['href'],
            'publisher': info2[0].strip(),
            'volume': cast(info2[1].split(':')[-1]),
            'issue': cast(info2[2].split(':')[-1]),
            'date': date,
            'type': info2[4].strip(),
            'quartile': cast(quartile[1]) if re.search(r'^Q[1-4]{1}$', quartile) else '-',
            'citations': cast(citations) if is_integer(citations) else 0
        })

    return result
