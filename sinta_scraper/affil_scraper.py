from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils


def affil(affil_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    worker_result = []

    worker(affil_id, worker_result)

    return utils.format_output(worker_result[0], output_format, pretty_print, xml_library)


def affils(affil_ids, output_format='dictionary', pretty_print=None, xml_library='dicttoxml', max_workers=None):
    worker_result = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for affil_id in affil_ids:
            executor.submit(worker, affil_id, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(affil_id, worker_result):
    url = f'http://sinta.ristekbrin.go.id/affiliations/detail?id={affil_id}&view=overview'
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


if __name__ == '__main__':
    print(affil('404', output_format='json', pretty_print=True))
