import threading
import re
from bs4 import BeautifulSoup
from requests import get

import utils


def author_researches(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=research'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = int(page_info[0].text.strip().split()[3])
    threads = []
    worker_result = []

    # for page in range(1, n_page + 1):
    for page in range(1, 2):
        thread = threading.Thread(target=worker, args=(author_id, page, worker_result))

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    page_url = f'http://sinta.ristekbrin.go.id/authors/detail?page={page}&id={author_id}&view=research'
    page_html = get(page_url)
    page_soup = BeautifulSoup(page_html.content, 'html.parser')
    trs = page_soup.select('table.uk-table tr')

    for tr in trs:
        link = tr.select('a.paper-link')

        if not link:
            continue

        link = link[0]
        info1 = tr.select('dd.indexed-by-orange')[0].text.strip().split('|')
        dd = tr.select('dd')
        info2 = [i.strip().split(':')[1].strip() for i in dd[2].text.strip().split('\r\n')]
        members = [member.strip() for member in dd[1].text.split(',') if member.strip()]

        worker_result.append({
            'title': link.text.strip(),
            'scheme': info1[0].split(':')[1].strip(),
            'source': info1[1].split(':')[1].strip(),
            'members': members,
            'application_year': int(info2[0]),
            'event_year': int(info2[1]),
            'fund': int(re.sub('[Rp\.\s\,]', '', info2[2])[:-2]),
            'field': dd[3].text.strip()
        })
