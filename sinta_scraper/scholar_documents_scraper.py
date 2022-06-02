from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get
from string_utils.validation import is_integer

from utils.config import get_config
from utils.utils import cast, format_output, listify


def author_scholar_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                        min_year=None, max_year=None, max_workers=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentsgs'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = cast(page_info[0].text.strip().split()[3])
    worker_result = author_scholar_parser(soup)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(author_scholar_worker, author_id, page, worker_result)

    if min_year is not None:
        worker_result = [doc for doc in worker_result if is_integer(str(doc['year'])) and doc['year'] >= min_year]

    if max_year is not None:
        worker_result = [doc for doc in worker_result if is_integer(str(doc['year'])) and doc['year'] <= max_year]

    return format_output(worker_result, output_format, pretty_print, xml_library)


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

    for row in rows:
        link = row.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        authors = row.select('dd')[0].text.split(', ')
        info = row.select('dd.indexed-by')[0].text.strip().split('|')
        citations = row.select('.index-val')[1].text.strip()

        result.append({
            'title': link.text,
            'authors': authors,
            'url': link['href'],
            'publisher': info[0].strip(),
            'year': cast(info[3].strip()),
            'citations': cast(citations) if is_integer(citations) else 0
        })

    return result


def dept_scholar(dept_ids, affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                 min_year=None, max_year=None):
    dept_ids = listify(dept_ids)
    worker_result = []

    for dept_id in dept_ids:
        domain = get_config()['domain']
        url = f'{domain}/departments/detail?afil={affil_id}&id={dept_id}&view=documents'
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        page_info = soup.select('.uk-width-large-1-2.table-footer')
        n_page = cast(page_info[0].text.strip().split()[3])

        worker_result.extend(dept_scholar_parser(soup))

        with ThreadPoolExecutor() as executor:
            for page in range(2, n_page + 1):
                executor.submit(dept_scholar_worker, dept_id, affil_id, page, min_year, max_year, worker_result)

    print(len(worker_result))
    return format_output(worker_result, output_format, pretty_print, xml_library)


def dept_scholar_worker(dept_id, affil_id, page, min_year, max_year, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/departments/detail?page={page}&id={dept_id}&afil={affil_id}&view=documents'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    result = dept_scholar_parser(soup)

    worker_result.extend(result)


def dept_scholar_parser(soup):
    rows = soup.select('table.uk-table tr')
    result = []

    for row in rows:
        link = row.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        authors = row.select('dd')[0].text.split(', ')
        info = row.select('dd.indexed-by')[0].text.strip().split('|')
        citations = row.select('.index-val')[1].text.strip()

        result.append({
            'title': link.text,
            'authors': authors,
            'url': link['href'],
            'publisher': info[0].strip(),
            'year': cast(info[3].strip()),
            'citations': cast(citations) if is_integer(citations) else 0
        })

    return result


if __name__ == '__main__':
    # dept_ids = 55201, 57201, 59201, 83207, 56201, 55101
    dept_ids = 55101
    affil_id = 404

    print(dept_scholar(dept_ids, affil_id, output_format='json', pretty_print=True))
