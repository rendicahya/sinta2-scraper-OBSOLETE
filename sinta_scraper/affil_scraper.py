import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils
from utils.config import get_config


def affil(affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    worker_result = []

    affil_worker(affil_id, worker_result)

    return utils.format_output(worker_result[0], output_format, pretty_print, xml_library)


def affils(affil_ids, output_format='dictionary', pretty_print=None, xml_library='dicttoxml', max_workers=None):
    worker_result = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for affil_id in affil_ids:
            executor.submit(affil_worker, affil_id, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def affil_worker(affil_id, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/affiliations/detail?id={affil_id}&view=overview'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    name = soup.select('.au-name')[0].text.strip()
    affil_url = soup.select('.au-department > a')[0].text.strip()

    stats = [utils.cast(soup.select('.stat2-val')[i].text.strip().replace(',', '')) for i in range(9)]

    result_data = {
        'name': name,
        'url': affil_url,
        'score': {
            'overall': stats[0],
            'overall_v2': stats[1],
            '3_years': stats[3],
            '3_years_v2': stats[4]
        },
        'rank': {
            'national': stats[2],
            '3_years_national': stats[5]
        },
        'journals': stats[6],
        'verified_authors': stats[7],
        'lecturers': stats[8]
    }

    worker_result.append(result_data)


def affil_authors(affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml',
                  max_workers=None):
    domain = get_config()['domain']
    url = f'{domain}/affiliations/detail?id={affil_id}&view=authors'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    n_page = utils.cast(page_info[0].text.strip().split()[3])
    worker_result = author_parser(soup)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(2, n_page + 1):
            executor.submit(affil_authors_worker, affil_id, page, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def affil_authors_worker(affil_id, page, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/affiliations/detail?page={page}&view=authors&id={affil_id}&sort=year2'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    data = author_parser(soup)

    worker_result.extend(data)


def author_parser(soup):
    rows = soup.select('.uk-description-list-line')
    result = []

    for row in rows:
        link = row.select('.text-blue')[0]
        author_id = re.search(r'id=(\d+)', link['href'].strip()).group(1)
        author_name = link.text.strip()
        nidn = row.select('dd')[1].text.split()[-1]

        result.append({
            'id': author_id,
            'name': author_name.title(),
            'nidn': nidn
        })

    return result
