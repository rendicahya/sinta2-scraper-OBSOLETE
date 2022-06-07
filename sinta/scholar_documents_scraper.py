import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get
from string_utils.validation import is_integer

from utils.config import get_config
from utils.utils import cast, format_output, listify


def author_scholar(author_id, output_format='dictionary', min_year=None, max_year=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentsgs'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = cast(page_info[0].text.strip().split()[3])
    worker_result = author_scholar_parser(soup)

    with ThreadPoolExecutor() as executor:
        for page in range(2, n_page + 1):
            executor.submit(author_scholar_worker, author_id, page, worker_result)

    if min_year is not None:
        worker_result = [doc for doc in worker_result if is_integer(str(doc['year'])) and doc['year'] >= min_year]

    if max_year is not None:
        worker_result = [doc for doc in worker_result if is_integer(str(doc['year'])) and doc['year'] <= max_year]

    return format_output(worker_result, output_format)


def author_scholar_worker(author_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=documentsgs'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data = author_scholar_parser(soup)

    worker_result.extend(data)


def author_scholar_parser(soup):
    rows = soup.select('table.uk-table tr')
    result = []
    publisher_regex = re.compile(r'([A-Za-z ]+)\s*(\d+)\s*\((\d+)\)[,\s]*(\d+-*\d*)[,\s]*(\d{4})*')

    for row in rows:
        link = row.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        authors = row.select('dd')[0].text.split(', ')
        info = row.select('dd.indexed-by')[0].text.strip().split('|')
        citations = row.select('.index-val')[1].text.strip()
        publisher_full = info[0].strip()
        publisher_parsed = publisher_regex.search(publisher_full)

        if publisher_parsed:
            fields = 'full', 'name', 'volume', 'issue', 'pages', 'year'
            publisher = {field: cast(publisher_parsed.group(i)) for i, field in enumerate(fields)}
        else:
            publisher = publisher_full

        result.append({
            'title': link.text,
            'authors': authors,
            'url': link['href'],
            'publisher': publisher,
            'year': cast(info[3].strip()),
            'citations': cast(citations) if is_integer(citations) else 0
        })

    return result


def dept_scholar(dept_ids, affil_id, output_format='dictionary', min_year=None, max_year=None):
    dept_ids = listify(dept_ids)
    worker_result = []

    for dept_id in dept_ids:
        domain = get_config()['domain']
        url = f'{domain}/departments/detail?afil={affil_id}&id={dept_id}&view=documents'
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        page_info = soup.select('.uk-width-large-1-2.table-footer')
        n_page = cast(page_info[0].text.strip().split()[3])

        worker_result.extend(dept_scholar_parser(soup, min_year, max_year))

        with ThreadPoolExecutor() as executor:
            for page in range(2, n_page + 1):
                executor.submit(dept_scholar_worker, dept_id, affil_id, page, min_year, max_year, worker_result)

    return format_output(worker_result, output_format)


def dept_scholar_worker(dept_id, affil_id, page, min_year, max_year, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/departments/detail?page={page}&id={dept_id}&afil={affil_id}&view=documents'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    result = dept_scholar_parser(soup, min_year, max_year)

    worker_result.extend(result)


def dept_scholar_parser(soup, min_year, max_year):
    rows = soup.select('table.uk-table tr')
    result = []
    publisher_regex = re.compile(r'([A-Za-z ]+)\s*(\d+)\s*\((\d+)\)[,\s]*(\d+-*\d*)[,\s]*(\d{4})*')

    for row in rows:
        link = row.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        authors = row.select('dd')[0].text.split(', ')
        info = row.select('dd.indexed-by')[0].text.strip().split('|')
        citations = row.select('.index-val')[1].text.strip()
        year = cast(info[3].strip())
        publisher_full = info[0].strip()
        publisher_parsed = publisher_regex.search(publisher_full)

        if publisher_parsed:
            fields = 'full', 'name', 'volume', 'issue', 'pages', 'year'
            publisher = {field: cast(publisher_parsed.group(i)) for i, field in enumerate(fields)}
        else:
            publisher = publisher_full

        if (min_year is not None and is_integer(str(year)) and int(year) < min_year) or (
                max_year is not None and is_integer(str(year)) and int(year) > min_year):
            continue

        result.append({
            'title': link.text,
            'authors': authors,
            'url': link['href'],
            'publisher': publisher,
            'year': cast(info[3].strip()),
            'citations': cast(citations) if is_integer(citations) else 0
        })

    return result
