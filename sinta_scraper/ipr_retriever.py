import threading

from bs4 import BeautifulSoup
from requests import get

import utils


def author_ipr(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=ipr'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = int(page_info[0].text.strip().split()[3])
    threads = []
    worker_result = []

    for page in range(1, n_page + 1):
        thread = threading.Thread(target=worker, args=(author_id, page, worker_result))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    page_url = f'http://sinta.ristekbrin.go.id/authors/detail?page={page}&id={author_id}&view=ipr'
    page_html = get(page_url)
    page_soup = BeautifulSoup(page_html.content, 'html.parser')
    trs = page_soup.select('table.uk-table tr')

    for tr in trs:
        h4 = tr.select('h4.uk-text-primary')

        if not h4:
            continue

        h4 = h4[0]
        info = tr.select('.uk-text-success')

        worker_result.append({
            'id': info[0].text.strip(),
            'title': h4.text.strip(),
            'category': info[1].text.strip(),
            'year': info[2].text.strip(),
            'holder': info[3].text.strip()
        })
