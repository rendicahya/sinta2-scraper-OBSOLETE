from requests import get
from bs4 import BeautifulSoup
import re


def get_author(author_id):
    url = f'http://sinta.ristekbrin.go.id/authors/detail?id={author_id}&view=overview'
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    author_name = soup.select('.au-name')[0].text.title()

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
        }
    }


author = get_author(5999838)

print(author)
