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
    worker_result = []

    for page in range(1, n_page + 1):
        thread = threading.Thread(target=author_scholar_docs_worker, args=(author_id, page, worker_result))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def author_scholar_docs_worker(author_id, page, worker_result):
    page_url = f'http://sinta.ristekbrin.go.id/authors/detail?page={page}&id={author_id}&view=documentsgs'
    page_html = get(page_url)
    page_soup = BeautifulSoup(page_html.content, 'html.parser')
    trs = page_soup.select('table.uk-table tr')

    for tr in trs:
        link = tr.select('a.paper-link')

        if len(link) < 1:
            continue

        link = link[0]

        info = tr.select('dd.indexed-by')[0].text.strip().split('|')
        publisher = info[0].strip()
        year = int(info[3].strip())

        worker_result.append({
            'title': link.text,
            'url': link['href'],
            'publisher': publisher,
            'year': year
        })
