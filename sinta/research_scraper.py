import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils
from sinta.dept_scraper import dept_authors
from utils.config import get_config


def author_researches(author_id, output_format='dictionary'):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=research'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = utils.cast(page_info[0].text.strip().split()[3])
    worker_result = parse(soup)

    with ThreadPoolExecutor() as executor:
        for page in range(2, n_page + 1):
            executor.submit(author_researches_worker, author_id, page, worker_result)

    return utils.format_output(worker_result, output_format)


def author_researches_worker(author_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?page={page}&id={author_id}&view=research'
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
            'application_year': utils.cast(info2[0]),
            'event_year': utils.cast(info2[1]),
            'fund': utils.cast(re.sub(r'[Rp\.\s\,]', '', info2[2])[:-2]),
            'field': dd[3].text.strip(),
            'sponsor': row.select('td.uk-text-center')[0].text.strip()
        })

    return result


def dept_researches(dept_ids, affil_id, output_format='dictionary'):
    if type(dept_ids) is not list and type(dept_ids) is not tuple:
        dept_ids = [dept_ids]

    authors = []
    worker_result = []

    for dept_id in dept_ids:
        authors.extend(dept_authors(dept_id, affil_id))

    with ThreadPoolExecutor() as executor:
        for author in authors:
            executor.submit(dept_researches_worker, author['id'], worker_result)

    return utils.format_output(worker_result, output_format)


def dept_researches_worker(author_id, worker_result):
    researches = author_researches(author_id)

    worker_result.extend(researches)
