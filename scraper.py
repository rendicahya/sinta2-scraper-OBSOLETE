import re

from bs4 import BeautifulSoup
from requests import get


def get_author(author_id):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=overview'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    author_name = soup.select('.au-name')[0].text.title()
    author_areas = [area.text for area in soup.select('.area-item')]
    author_scores_soup = soup.select('.stat2-val')
    score_names = ['overall', '3_years', 'overall_v2', '3_years_v2', 'books',
                   'national_rank', '3_years_national_rank', 'ipr',
                   'affiliation_rank', '3_years_affiliation_rank']

    author_scores = {score_name: float(author_scores_soup[i].text) for i, score_name in enumerate(score_names)}

    affiliation = soup.select('.au-affil > a')
    affiliation_name = affiliation[0].text
    affiliation_url = 'http://sinta.ristekbrin.go.id/' + affiliation[0]['href']
    affiliation_id = re.search(r'id=(\d+)', affiliation_url).group(1)

    return {
        'id': author_id,
        'name': author_name,
        'url': url,
        'affiliation': {
            'id': affiliation_id,
            'name': affiliation_name,
            'url': affiliation_url
        },
        'areas': author_areas,
        'scores': author_scores
    }


def get_dept_authors(dept_id):
    url = f'http://sinta.ristekbrin.go.id/departments/detail?afil=404&id={dept_id}&view=authors'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_info = soup.select('.uk-width-large-1-2.table-footer')
    max_page = int(page_info[0].text.strip().split()[3])
    author_ids = []

    for page in range(1, max_page + 1):
        page_url = f'http://sinta.ristekbrin.go.id/departments/detail?page={page}&afil=404&id={dept_id}&view=authors&sort=year2'
        page_html = get(page_url)
        page_soup = BeautifulSoup(page_html.content, 'html.parser')
        authors = page_soup.select('a.text-blue')
        page_author_ids = [re.search(r'id=(\d+)', author['href']).group(1) for author in authors]

        author_ids.extend(page_author_ids)

    return author_ids
