# Sinta Scraper

Retrieves information from Sinta (http://sinta.ristekbrin.go.id) via scraping.

## Code Sample
Code sample for all functions is available as a Google Colab Notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rendicahya/sinta-scraper/blob/master/sinta-scraper-sample.ipynb)

## Installation
`pip install sinta-scraper`

Dependencies: `bs4`, `requests`, `dicttoxml`, and `dict2xml`. These will be automatically installed by pip with the above command.

## Importing
`import sinta_scraper as sinta`

## Available Functions
- ### `author()`
Retrieves a single author's information by Sinta ID. For example:
```
author_id = '5975467'
author = sinta.author(author_id)

print(author['name'])
# Output: Agus Zainal Arifin
```

The output format is the Python dictionary. The structure is given in the following sample output.
```
{
    'id': '5975467',
    'name': 'AGUS ZAINAL ARIFIN',
    'url': 'http://sinta.ristekbrin.go.id/authors/detail?id=5975467&view=overview',
    'affiliation': {
        'id': '417',
        'name': 'Institut Teknologi Sepuluh Nopember',
        'url': 'http://sinta.ristekbrin.go.id/affiliations/detail/?id=417&view=overview'
    },
    'department': 'Teknik Informatika',
    'areas': [
        'computer vision',
        'image processing',
        'information retrieval',
        'medical imaging',
        'machine learning'
    ],
    'score': {
        'overall': 38.24,
        '3_years': 8.36,
        'overall_v2': 3485.0,
        '3_years_v2': 1345.0
    },
    'rank': {
        'national': 596,
        '3_years_national': 509,
        'affiliation': 28,
        '3_years_affiliation': 22
    },
    'scopus': {
        'documents': 52,
        'citations': 355,
        'h-index': 8,
        'i10-index': 6,
        'g-index': 14,
        'articles': 28,
        'conferences': 24,
        'others': 0,
        'Q1': 5,
        'Q2': 11,
        'Q3': 9,
        'Q4': 2,
        'undefined': 25
    },
    'scholar': {
        'documents': 232,
        'citations': 1087,
        'h-index': 13,
        'i10-index': 25,
        'g-index': 25
    },
    'wos': {
        'documents': 1,
        'citations': null,
        'h-index': null,
        'i10-index': null,
        'g-index': null
    },
    'sinta': {
        'S0': 1,
        'S1': 3,
        'S2': 1,
        'S3': 2,
        'S4': 0,
        'S5': 0,
        'uncategorized': 225
    },
    'books': 0,
    'ipr': 2
}
```

- ### `authors()`
Retrieves several author's information by Sinta ID. For example:
```
author_ids = ['5975467', '6005015', '29555']
authors = sinta.authors(author_ids)

print(authors[1]['name'])
# Output: MAURIDHI HERY PURNOMO
```

The output is a list of dictionaries with the same structure given by the `author()` function.

### - `dept_authors()`
Retrieves a list of authors associated with a department. Department ID and affiliation ID must be specified. The output structure is different from that given by the previous function. This function retrieves only the ID's and names of each author. For example:
```
dept_id = '55001'
affil_id = '417'
authors = sinta.dept_authors(dept_id, affil_id)

print(authors[:3])
# Output: [{'id': '29555', 'name': 'Riyanarto Sarno'}, {'id': '5975467', 'name': 'Agus Zainal Arifin'}, {'id': '6023328', 'name': 'Nanik Suciati'}]
```

### - `depts_authors()`
Does the same thing as `dept_authors()` except that you can specify a list of department ID's as argument. For example:
```
dept_ids = ['55001', '20201', '24201']
affil_id = '417'
authors = sinta.depts_authors(dept_ids, affil_id)

print(authors[:-3])
# Output: [{'id': '6674726', 'name': 'Cahayahati'}, {'id': '6690103', 'name': 'Ari Santoso'}, {'id': '6199111', 'name': 'Lucky Putri Rahayu'}]
```

## Other Output Formats
Other formats can be used by specifying the `output_format` argument:
```
author = sinta.author(id, output_format='json')
```

Avalable output formats:
- `'dictionary'` (default)
- `'json'`
- `'xml'`

JSON output can be pretty-printed by setting `pretty_print=True`:
```
author = sinta.author(id, output_format='json', pretty_print=True)
```

For XML output, there are two library options which can be specified in the `xml_library` argument. These libraries give different output formats. The options are:
- `dicttoxml` (default)
- `dict2xml`

For example:
```
author = sinta.author(id, output_format='xml', xml_library='dict2xml')
```

If you want the XML output to be pretty-printed, you need to choose `dict2xml` instead of `xmltodict` since the latter does not produce pretty-printed XML output.

### Todo
- Other output formats: CSV.
- `affil(affil_id)` function.
- `find_affil(keyword)` function.
- `affil_depts(affil_id)` function.
- `affil_authors(affil_id)` function.
- `dept(dept_id)` function.
- `find_dept(keyword)` function.
- `author_scopus_docs(author_id)` function.
- `author_wos_docs(author_id)` function.
- `author_books(author_id)` function.
