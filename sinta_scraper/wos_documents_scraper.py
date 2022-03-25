from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils
from config import get_config


def author_wos_docs(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                    max_workers=None):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=documentswos'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = utils.cast(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(worker, author_id, page, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=documentswos'
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
        info1 = row.select('dd.indexed-by')[0].text.strip().split('|')
        info2 = row.select('dd')[0].text.strip().split('\n')
        issn = info2[1].split(':')[1].strip()
        doi = info2[2].split(':')[1].strip()
        uid = info2[3].split(' : ')[1].strip()

        result.append({
            'title': link.text,
            'publisher': info1[0].strip(),
            'issn': issn if issn else '-',
            'doi': doi if doi else '-',
            'uid': uid if uid else '-'
        })

    return result
