import threading

from bs4 import BeautifulSoup
from requests import get

import utils


def author_scholar_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=documentsgs'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = int(page_info[0].text.strip().split()[3])
    threads = []
    worker_result = parse(soup)

    for page in range(2, n_page + 1):
        thread = threading.Thread(target=worker, args=(author_id, page, worker_result))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    page_url = f'http://sinta.ristekbrin.go.id/authors/detail?page={page}&id={author_id}&view=documentsgs'
    page_html = get(page_url)
    page_soup = BeautifulSoup(page_html.content, 'html.parser')
    data = parse(page_soup)

    worker_result.extend(data)


def parse(soup):
    trs = soup.select('table.uk-table tr')
    result = []

    for tr in trs:
        link = tr.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        info = tr.select('dd.indexed-by')[0].text.strip().split('|')
        publisher = info[0].strip()
        year = int(info[3].strip())

        result.append({
            'title': link.text,
            'url': link['href'],
            'publisher': publisher,
            'year': year
        })

    return result
