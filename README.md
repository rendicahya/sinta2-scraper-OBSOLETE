# Sinta Scraper

Retrieves information from Sinta (http://sinta.ristekbrin.go.id) via scraping.

## Installation
`pip install sinta-scraper`

Dependencies: bs4, requests, dicttoxml, dict2xml. These will be automatically installed by pip with the above command.

## Usage

### Import
`import sinta-scraper as sinta`

### Get author information by Sinta ID
```
id = '5975467'
author = sinta.author(id)
```

### Output
The default output is Python dictionary. The structure is given in the following sample output.
```
{'id': '5975467',
 'name': 'Agus Zainal Arifin',
 'url': 'http://sinta.ristekbrin.go.id/authors/detail?id=5975467&view=overview',
 'affiliation': {'id': '417',
                 'name': 'Institut Teknologi Sepuluh Nopember',
                 'url': 'http://sinta.ristekbrin.go.id//affiliations/detail/?id=417&view=overview'},
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

If you want the XML output to be pretty-printed, you need to choose `dict2xml` since `xmltodict` does not produce pretty-printed XML output.

### Available Functions
- `author(sinta_id)`: gets an author's information. 
- `dept_authors(dept_id)`: gets authors associated with a department.

### Todo
- Other output formats: CSV.
- `affil(affil_id)` function.
- `find_affil(keyword)` function.
- `affil_depts(affil_id)` function.
- `affil_authors(affil_id)` function.
- `dept(dept_id)` function.
- `find_dept(keyword)` function.
