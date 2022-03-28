import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils
from utils.config import get_config


def author(author_id, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    worker_result = []

    worker(author_id, worker_result)

    return utils.format_output(worker_result[0], output_format, pretty_print, xml_library)


def authors(author_ids, output_format='dictionary', pretty_print=None, xml_library='dicttoxml', max_workers=None):
    worker_result = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for author_id in author_ids:
            executor.submit(worker, author_id, worker_result)

    return utils.format_output(worker_result, output_format, pretty_print, xml_library)


def worker(author_id, worker_result):
    domain = get_config()['domain']
    url = f'{domain}/authors/detail?id={author_id}&view=overview'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    name = soup.select('.au-name')[0].text.strip()
    areas = [area.text.strip() for area in soup.select('.area-item')]
    scores_soup = soup.select('.stat2-val')

    index_score_names = ['documents', 'citations', 'h-index', 'i10-index', 'g-index']
    index_scores = soup.select('.stat-num-pub')

    scopus = {index_score_names[i]: utils.cast(index_scores[i + 16].text) for i in range(len(index_score_names))}
    scopus_outputs_names = ['articles', 'conferences', 'others']
    scopus_outputs = {scopus_outputs_names[i]: utils.cast(soup.select('.stat-num-pub')[i].text) for i in range(3)}
    scopus_quartiles = {f'Q{i}': utils.cast(soup.select('.stat-num-pub')[i + 3].text) for i in range(1, 5)}
    scopus = {**scopus, **scopus_outputs, **scopus_quartiles}
    scopus['undefined'] = utils.cast(soup.select('.stat-num-pub')[8].text)

    scholar = {index_score_names[i]: utils.cast(index_scores[i + 21].text) for i in range(len(index_score_names))}
    wos = {index_score_names[i]: utils.cast(index_scores[i + 26].text) for i in range(len(index_score_names))}

    sinta = {f'S{i}': utils.cast(index_scores[i + 9].text) for i in range(6)}
    sinta['uncategorized'] = utils.cast(index_scores[15].text)

    score_names = ['overall', '3_years', 'overall_v2', '3_years_v2']
    scores = {score_name: float(scores_soup[i].text) for i, score_name in enumerate(score_names)}

    books = utils.cast(scores_soup[4].text)
    ipr = utils.cast(scores_soup[7].text)

    rank_names = ['national', '3_years_national', 'ipr', 'affiliation', '3_years_affiliation']
    ranks = {rank_names[i]: utils.cast(scores_soup[i + 5].text) for i in [0, 1, 3, 4]}

    affil = soup.select('.au-affil > a')
    dept = soup.select('.au-department')[0].text.strip()
    affil_name = affil[0].text.strip()
    affil_url = 'http://sinta.ristekbrin.go.id' + affil[0]['href']
    affil_id = re.search(r'id=(\d+)', affil_url).group(1)

    result_data = {
        'id': author_id,
        'name': name,
        'url': url,
        'affiliation': {
            'id': affil_id,
            'name': affil_name,
            'url': affil_url
        },
        'department': dept,
        'areas': areas,
        'score': scores,
        'rank': ranks,
        'scopus': scopus,
        'scholar': scholar,
        'wos': wos,
        'sinta': sinta,
        'books': books,
        'ipr': ipr
    }

    worker_result.append(result_data)
