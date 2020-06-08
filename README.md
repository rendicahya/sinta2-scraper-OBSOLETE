# Sinta Scraper

Retrieves information from Sinta (http://sinta.ristekbrin.go.id) via scraping.

## Installation
`pip install sinta-scraper`

Dependencies: `bs4`, `requests`, `dicttoxml`, and `dict2xml`. These will be automatically installed by pip with the above command.

## Importing
`import sinta-scraper as sinta`

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
{'id': '5975467',
 'name': 'Agus Zainal Arifin',
 'url': 'http://sinta.ristekbrin.go.id/authors/detail?id=5975467&view=overview',
 'affiliation': {'id': '417',
                 'name': 'Institut Teknologi Sepuluh Nopember',
                 'url': 'http://sinta.ristekbrin.go.id/affiliations/detail/?id=417&view=overview'},
 'areas': ['computer vision',
           'image processing',
           'information retrieval',
           'medical imaging',
           'machine learning'],
 'score': {'overall': 36.9,
           '3_years': 7.26,
           'overall_v2': 3304.0,
           '3_years_v2': 1284.5},
 'rank': {'national': 614,
          '3_years_national': 472,
          'affiliation': 26,
          '3_years_affiliation': 21},
 'scopus': {'documents': '50',
            'citations': '341',
            'h-index': '8',
            'i10-index': '6',
            'g-index': '14'},
 'scholar': {'documents': '220',
             'citations': '1067',
             'h-index': '13',
             'i10-index': '23',
             'g-index': '25'},
 'books': 0,
 'ipr': 2}
```

- ### `authors()`
Retrieves several author's information by Sinta ID. For example:
```
author_ids = ['5975467', '6005015', '29555']
authors = sinta.authors(author_ids)

print(authors[1]['name'])
# Output: Mauridhi Hery Purnomo
```

The output is a list of dictionaries with the same structure given by the `author()` function.

### - `dept_authors()`
Retrieves a list of authors associated with a department. Department ID and affiliation ID must be specified. The output structure is different from that given by the previous function. This function retrieves only the ID's and names of each author. For example:
```
dept_id = '55001'
affil_id = '417'
authors = sinta.dept_authors(dept_id, affil_id)

print(authors[:3)
# Output: [{'id': '29555', 'name': 'Riyanarto Sarno'}, {'id': '5975467', 'name': 'Agus Zainal Arifin'}, {'id': '6023328', 'name': 'Nanik Suciati'}]
```

### Other Output Formats
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
