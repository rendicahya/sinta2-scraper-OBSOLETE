import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils


def author_researches(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                      max_workers=None):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=research'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = int(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(worker, author_id, page, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, page, worker_result):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?page={page}&id={author_id}&view=research'
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
        info1 = row.select('dd.indexed-by-orange')[0].text.split('|')
        dd = row.select('dd')
        info2 = [i.split(':')[1].strip() for i in dd[2].text.strip().split('\r\n')]
        members = [member.strip() for member in dd[1].text.split(',') if member.strip()]

        result.append({
            'title': link.text.strip(),
            'scheme': info1[0].split(':')[1].strip(),
            'source': info1[1].split(':')[1].strip(),
            'members': members,
            'application_year': int(info2[0]),
            'event_year': int(info2[1]),
            'fund': int(re.sub(r'[Rp\.\s\,]', '', info2[2])[:-2]),
            'field': dd[3].text.strip(),
            'sponsor': row.select('td.uk-text-center')[0].text.strip()
        })

    return result
