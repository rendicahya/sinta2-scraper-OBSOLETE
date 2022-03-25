# Sinta Scraper

Retrieves information from Sinta (https://sinta.kemdikbud.go.id) via scraping.

## Code Sample
Code sample for all functions is available as a Google Colab notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rendicahya/sinta-scraper/blob/master/sinta-scraper-sample.ipynb)

## Installation
`pip install sinta-scraper`

Dependencies: `bs4`, `requests`, `dicttoxml`, `dict2xml`, and `yaml-helper`.

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

- ### `dept_authors()`
Retrieves a list of authors associated with a department. Department ID and affiliation ID must be specified. The output structure is different from that given by the previous function. This function retrieves only the ID's and names of each author. For example:
```
dept_id = '55001'
affil_id = '417'
authors = sinta.dept_authors(dept_id, affil_id)

print(authors[:3])
# Output: [{'id': '29555', 'name': 'Riyanarto Sarno'}, {'id': '5975467', 'name': 'Agus Zainal Arifin'}, {'id': '6023328', 'name': 'Nanik Suciati'}]
```

- ### `depts_authors()`
Does the same thing as `dept_authors()` except that you can specify a list of department ID's as argument. For example:
```
dept_ids = ['55001', '20201', '24201']
affil_id = '417'
authors = sinta.depts_authors(dept_ids, affil_id)

print(authors[:-3])
# Output: [{'id': '6674726', 'name': 'Cahayahati'}, {'id': '6690103', 'name': 'Ari Santoso'}, {'id': '6199111', 'name': 'Lucky Putri Rahayu'}]
```

- ### `affil()`
Retrieves information about an affiliation. For example:

```
affil_id = '417'
affil = sinta.affil(affil_id)

print(affil)

# Output:
{
    'name': 'Institut Teknologi Sepuluh Nopember',
    'url': 'https://its.ac.id',
    'score': {
        'overall': 34332,
        'overall_v2': 514402,
        '3_years': 6569,
        '3_years_v2': 202157
    },
    'rank': {
        'national': 7,
        '3_years_national': 10
    },
    'journals': 18,
    'verified_authors': 1084,
    'lecturers': 961
}
```

- ### `affils()`
Retrieves information about several affiliations. For example:
```
affil_ids = ['417', '404']
affils = sinta.affils(affil_ids)

print(affils)

# Output:
[
    {
        'name': 'Institut Teknologi Sepuluh Nopember',
        'url': 'https://its.ac.id',
        'score': {
            'overall': 34332,
            'overall_v2': 514402,
            '3_years': 6569,
            '3_years_v2': 202157
        },
        'rank': {
            'national': 7,
            '3_years_national': 10
        },
        'journals': 18,
        'verified_authors': 1084,
        'lecturers': 961
    },
    {
        'name': 'Universitas Brawijaya',
        'url': 'https://ub.ac.id/',
        'score': {
            'overall': 43734,
            'overall_v2': 513660,
            '3_years': 7443,
            '3_years_v2': 245747
        },
        'rank': {
            'national': 8,
            '3_years_national': 5
        },
        'journals': 60,
        'verified_authors': 2245,
        'lecturers': 2054
    }
]
```

- ### `affil_authors()`
Retrieves authors associated with the specified affiliation. For example:
```
affil_id = '417'
authors = sinta.affil_authors(affil_id)

print(authors)

# Output: [{'id': '29555', 'name': 'Riyanarto Sarno', 'nidn': '0003085905'}, {'id': '6005015', 'name': 'Mauridhi Hery Purnomo', 'nidn': '0016095811'}]
```

- ### `author_researches()`
Retrieves an author's researches. For example:
```
author_id = '6005015'
researches = sinta.author_researches(author_id)

print(researches[:2])

# Output:
[
    {
        'title': 'Monitoring Kestabilan Transient dengan Mempertimbangkan Parameter Sudut Rotor, Frekuensi, dan Tegangan Berbasis Computational Intelligence',
        'scheme': 'Penelitian Penugasan ( WCR )',
        'source': 'Simlitabmas',
        'members': [
            'Mauridhi Hery Purnomo',
            'Ardyono Priyadi',
            'Vita Lystianingrum B P'
        ],
        'application_year': 2020,
        'event_year': 2021,
        'fund': 118488700,
        'field': 'Energi',
        'sponsor': 'Ristekdikti'
    },
    {
        'title': 'Intelligent Teledermatology System untuk Smart Hospital',
        'scheme': 'Penelitian Penugasan ( KRU-PT )',
        'source': 'Simlitabmas',
        'members': [
            'I Ketut Eddy Purnama',
            'Anak Agung Putri Ratna',
            'Ingrid Nurtanio',
            'Afif Nurul Hidayati',
            'Reza Fuad Rachmadi',
            'Mauridhi Hery Purnomo',
            'Supeno Mardi Susiki Nugroho'
        ],
        'application_year': 2020,
        'event_year': 2021,
        'fund': 436800000,
        'field': 'Kesehatan',
        'sponsor': 'Ristekdikti'
    }
]
```

- ### `author_scholar_docs()`
Retrieves an author's Google Scholar items. For example:
```
author_id = '6005015'
scholar = sinta.author_scholar_docs(author_id)

print(scholar[:2])

# Output:
[
    {
        'title': 'Konsep pengolahan citra digital dan ekstraksi fitur',
        'url': 'https://scholar.google.com/scholar?oi=bibs&cluster=11975243569176755366&btnI=1&hl=en',
        'publisher': 'Yogyakarta:  Graha Ilmu; ISBN: 978-979-756-682-1 1 (2010), 280',
        'year': 2010,
        'citations': 0
    },
    {
        'title': 'Supervised Neural Networks dan Aplikasinya',
        'url': 'https://scholar.google.com/scholar?oi=bibs&cluster=4803627219094543302&btnI=1&hl=en',
        'publisher': 'Yogyakarta:  Graha Ilmu; ISBN: 978-979-756-123-9 1 (2006), 176',
        'year': 2006,
        'citations': 0
    }
]
```

- ### `author_scopus_docs()`
Retrieves an author's Scopus items. For example:
```
author_id = '6005015'
scopus = sinta.author_scopus_docs(author_id)

print(scopus[:2])

# Output:
[
    {
        'title': 'Controlling chaos and voltage collapse using an ANFIS-based composite controller-static var compensa',
        'url': 'https://www.scopus.com/record/display.uri?eid=2-s2.0-84869223917&origin=resultslist',
        'publisher': 'International Journal of Electrical Power and Energy Systems',
        'date': '2013-03-01',
        'type': 'Journal',
        'quartile': 1,
        'citations': 51
    },
    {
        'title': 'Adaptive modified firefly algorithm for optimal coordination of overcurrent relays',
        'url': 'https://www.scopus.com/record/display.uri?eid=2-s2.0-85026658931&origin=resultslist',
        'publisher': 'IET Generation, Transmission and Distribution',
        'date': '2017-07-13',
        'type': 'Journal',
        'quartile': 1,
        'citations': 38
    }
]
```

- ### `author_wos_docs()`
Retrieves an author's Web of Science items. For example:
```
author_id = '6005015'
wos = sinta.author_wos_docs(author_id)

print(wos[:2])

# Output:
[
    {
        'title': 'Adaptive B-spline neural network-based vector control for a grid side converter in wind turbine-DFIG systems',
        'publisher': 'IEEJ TRANSACTIONS ON ELECTRICAL AND ELECTRONIC ENGINEERING',
        'issn': '1931-4973',
        'doi': '-',
        'uid': 'WOS: 000362748500009'
    },
    {
        'title': 'ARIMA Modeling of Tropical Rain Attenuation on a Short 28-GHz Terrestrial Link',
        'publisher': 'IEEE ANTENNAS AND WIRELESS PROPAGATION LETTERS',
        'issn': '1536-1225',
        'doi': '10.1109/LAWP.2010.2046130',
        'uid': 'WOS: 000276520900002'
    }
]
```

- ### `author_comm_services()`
Retrieves an author's community service items. For example:
```
author_id = '5996278'
comm_svc = sinta.author_comm_services(author_id)

print(comm_svc)

# Output:
[
    {
        'title': 'IbM Pembelajaran Elektronik Untuk SMK',
        'scheme': 'Pengabdian Kepada Masyarakat Kompetitif Nasional ( PKM )',
        'source': 'Simlitabmas',
        'members': [
            'Candra Dewi',
            'Adharul Muttaqin',
            'Achmad Basuki'
        ],
        'application_year': 2015,
        'event_year': 2016,
        'fund': 50000000,
        'field': '',
        'sponsor': 'Ristekdikti'
    }
]
```

- ### `author_ipr()`
Retrieves an author's intellectual property right (IPR) items. For example:
```
author_id = '5996278'
ipr = sinta.author_ipr(author_id)

print(ipr)

# Output:
[
    {
        'id': 'EC00202016549',
        'title': 'Panduan Pembelajaran Daring Saat Kondisi Darurat COVID-19',
        'category': 'paten',
        'year': '2020',
        'holder': 'Universitas Brawijaya'
    }
]
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
- `find_affil(keyword)` function.
- `affil_depts(affil_id)` function.
- `dept(dept_id)` function.
- `find_dept(keyword)` function.
