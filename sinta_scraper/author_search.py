import re

from concurrent.futures import ThreadPoolExecutor

import bs4
from bs4 import BeautifulSoup
from requests import get

import utils

def search_author(term, output_format='dictionary', pretty_print=None, xml_library='dicttoxml'):
    '''
    Search the SINTA database for matching author name. 
    Input: author name (string)
    Output: library containing id, name, NIDN, affiliation, and research areas 
    '''
    worker_result = []

    worker(term, worker_result)

    return utils.format_output(worker_result[0], output_format, pretty_print, xml_library)

def worker(term, worker_result):
    result_data = get_author(term)
    worker_result.append(result_data)
    
def page_extractor(soup):
    '''
    extract information from each result page
    '''
    result = []
    for num, i in enumerate(soup.select(".text-blue")): #get first item
        #get name and sinta id
        name = i.text.strip()
        author_id = re.findall(r'\d+', i['href'])[0]
        # get affiliation and NIDN
        for x in i.find_next('dd'):
            affil_name = x.contents[0] 
            NIDN = x.find_next('dd').contents[2].replace(' : ', '')
        # Get expertise
        areas = [] # empty container
        expertise1 = i.find_next('a', {'class':"area-item-small"}) # get first expertise
        ctr = 0 # helper counter
        while ctr < 3 and isinstance(expertise1, bs4.element.Tag): # loop until NoneType & max 3 expertise
            areas.append(expertise1.contents[0])
            expertise1 = expertise1.find_next('a') # get next expertise
            try:
                if expertise1['class'][0] == 'area-item-small': # if expertise feature, continue
                    ctr = ctr + 1
                else: # if not expertise feature pass
                    ctr = 3
            except KeyError:
                ctr = 3
        
        result_data = {'id': author_id,
                       'name': name,
                       'NIDN' : NIDN,
                       'affiliation': affil_name,
                       'areas': areas 
                       }
        result.append(result_data)
    return result

def get_author(term):
    '''
    search author using term, iterate over pages, and retrive information
    '''
    term = term.replace(' ','+') #format search for url
    p_ctr = 1 # init page
    
    # load html from first page
    url = f'https://sinta.ristekbrin.go.id/authors?page={p_ctr}&q={term}&search=2&ag=&sort=year2&view='
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # calculate how many pages
    page = soup.find('caption').contents
    page = [int(s) for s in page[0].split() if s.isdigit()]
    p_max = page[1]
    
    # get result from first page
    result = []
    data = page_extractor(soup)
    [result.append(dic) for dic in data]
    
    # iterate over pages if result are multiple pages
    if p_max == 1:
        pass
    else:
        while p_ctr < (p_max + 1):
            p_ctr = p_ctr + 1
            print(f'{term}: retrieving page {p_ctr-1} of {p_max}')
            url = f'https://sinta.ristekbrin.go.id/authors?page={p_ctr}&q={term}&search=2&ag=&sort=year2&view='
            #print(url)
            html = get(url)
            soup = BeautifulSoup(html.content, 'html.parser')
            data = page_extractor(soup)
            [result.append(dic) for dic in data]
    return result


if __name__ == '__main__':
    print(search_author('Joko Widodo', output_format='json', pretty_print=True))