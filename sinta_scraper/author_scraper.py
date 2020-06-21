import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests import get

import utils


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
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=overview'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    name = soup.select('.au-name')[0].text.title()
    areas = [area.text for area in soup.select('.area-item')]
    scores_soup = soup.select('.stat2-val')

    index_score_names = ['documents', 'citations', 'h-index', 'i10-index', 'g-index']
    index_scores = soup.select('.stat-num-pub')

    scopus = {index_score_names[i]: utils.cast(index_scores[i + 16].text) for i in range(len(index_score_names))}
    scholar = {index_score_names[i]: utils.cast(index_scores[i + 21].text) for i in range(len(index_score_names))}

    score_names = ['overall', '3_years', 'overall_v2', '3_years_v2']
    scores = {score_name: float(scores_soup[i].text) for i, score_name in enumerate(score_names)}

    books = utils.cast(scores_soup[4].text)
    ipr = utils.cast(scores_soup[7].text)

    rank_names = ['national', '3_years_national', 'ipr', 'affiliation', '3_years_affiliation']
    ranks = {rank_names[i]: utils.cast(scores_soup[i + 5].text) for i in [0, 1, 3, 4]}

    affiliation = soup.select('.au-affil > a')
    affiliation_name = affiliation[0].text
    affiliation_url = 'http://sinta.ristekbrin.go.id' + affiliation[0]['href']
    affiliation_id = re.search(r'id=(\d+)', affiliation_url).group(1)

    result_data = {
        'id': author_id,
        'name': name,
        'url': url,
        'affiliation': {
            'id': affiliation_id,
            'name': affiliation_name,
            'url': affiliation_url
        },
        'areas': areas,
        'score': scores,
        'rank': ranks,
        'scopus': scopus,
        'scholar': scholar,
        'books': books,
        'ipr': ipr
    }

    worker_result.append(result_data)


if __name__ == '__main__':
    print(author('6082456', output_format='json', pretty_print=True))
