![](https://sinta.kemdikbud.go.id/assets/img/sinta_logo.png)

# Sinta Scraper

Retrieves information from Sinta (https://sinta.kemdikbud.go.id) via scraping.

## Code Sample

Code sample for all functions is available as a Google Colab
notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rendicahya/sinta-scraper/blob/master/sinta-scraper-sample.ipynb)
. Update: Sinta seems to be blocking accesses from Google Colab so you need to run the scripts locally.

## Installation

`pip install sinta-scraper`

Dependencies: `beautifulsoup4`, `requests`, `dicttoxml`, `dict2xml`, and `python-string-utils`.

## Importing

`import sinta_scraper as sinta`

## Available Functions

- [`affil()`](#affil)
- [`affils()`](#affils)
- [`affil_authors()`](#affil_authors)
- [`author()`](#author)
- [`author_researches()`](#author_researches)
- [`author_scholar_docs()`](#author_scholar_docs)
- [`author_scopus_docs()`](#author_scopus_docs)
- [`author_scopus_journal_docs()`](#author_scopus_journal_docs)
- [`author_scopus_conference_docs()`](#author_scopus_conference_docs)
- [`author_wos_docs()`](#author_wos_docs)
- [`author_comm_services()`](#author_comm_services)
- [`author_ipr()`](#author_ipr)
- [`dept_authors()`](#dept_authors)
- [`dept_researches()`](#dept_researches)
- [`dept_scholar_docs()`](#dept_scholar_docs)

## Function Details

- ### `affil()`

Retrieves information about an affiliation. For example:

```
affil_id = 417
affil = sinta.affil(affil_id)

print(affil)
```

Output:

```
{
    "name": "Institut Teknologi Sepuluh Nopember",
    "url": "https://its.ac.id",
    "score": {
        "overall": 37400,
        "overall_v2": 540707,
        "3_years": 5222,
        "3_years_v2": 182038
    },
    "rank": {
        "national": 7,
        "3_years_national": 11
    },
    "journals": 25,
    "verified_authors": 1115,
    "lecturers": 961
}
```

- ### `affils()`

Retrieves information about several affiliations. For example:

```
affil_ids = [417, 404]
affils = sinta.affils(affil_ids)

print(affils)
```

Output

```
[
    {
        "name": "Institut Teknologi Sepuluh Nopember",
        "url": "https://its.ac.id",
        "score": {
            "overall": 37400,
            "overall_v2": 540707,
            "3_years": 5222,
            "3_years_v2": 182038
        },
        "rank": {
            "national": 7,
            "3_years_national": 11
        },
        "journals": 25,
        "verified_authors": 1115,
        "lecturers": 961
    },
    {
        "name": "Universitas Brawijaya",
        "url": "www.ub.ac.id",
        "score": {
            "overall": 53982,
            "overall_v2": 538192,
            "3_years": 5946,
            "3_years_v2": 217740
        },
        "rank": {
            "national": 9,
            "3_years_national": 8
        },
        "journals": 67,
        "verified_authors": 2318,
        "lecturers": 2052
    }
]
```

- ### `affil_authors()`

Retrieves authors associated with the specified affiliation. This function usually takes more time to complete. For
example:

```
affil_id = 417
authors = sinta.affil_authors(affil_id)

print(authors[:5])
```

Output:

```
[
    {
        "id": "29555",
        "name": "Riyanarto Sarno",
        "nidn": "0003085905"
    },
    {
        "id": "6005015",
        "name": "Mauridhi Hery Purnomo",
        "nidn": "0016095811"
    },
    {
        "id": "5976088",
        "name": "Chastine Fatichah",
        "nidn": "0020127508"
    },
    {
        "id": "29653",
        "name": "Adhi Yuniarto",
        "nidn": "0001067304"
    },
    {
        "id": "5998915",
        "name": "Didik Prasetyoko",
        "nidn": "0016067108"
    }
]
```

- ### `author()`

Retrieves an author's information by Sinta ID. For example:

```
author_id = 5975467
author = sinta.author(author_id)

print(author)
```

The output format is the Python dictionary. The structure is given in the following sample output.

```
{
    "id": "5975467",
    "name": "AGUS ZAINAL ARIFIN",
    "url": "https://sinta.kemdikbud.go.id/authors/detail?id=5975467&view=overview",
    "affiliation": {
        "id": "417",
        "name": "Institut Teknologi Sepuluh Nopember",
        "url": "http://sinta.ristekbrin.go.id/affiliations/detail/?id=417&view=overview"
    },
    "department": "Teknik Informatika",
    "areas": [
        "computer vision",
        "image processing",
        "information retrieval",
        "medical imaging",
        "machine learning"
    ],
    "score": {
        "overall": 48.1,
        "3_years": 3.13,
        "overall_v2": 4726.0,
        "3_years_v2": 1377.5
    },
    "rank": {
        "national": 723,
        "3_years_national": 1099,
        "affiliation": 32,
        "3_years_affiliation": 30
    },
    "scopus": {
        "documents": 69,
        "citations": 469,
        "h-index": 10,
        "i10-index": 10,
        "g-index": 1,
        "articles": 39,
        "conferences": 30,
        "others": 0,
        "Q1": 6,
        "Q2": 12,
        "Q3": 13,
        "Q4": 3,
        "undefined": 35
    },
    "scholar": {
        "documents": 294,
        "citations": 1444,
        "h-index": 16,
        "i10-index": 36,
        "g-index": 31
    },
    "wos": {
        "documents": 1,
        "citations": null,
        "h-index": null,
        "i10-index": null,
        "g-index": null
    },
    "sinta": {
        "S0": 1,
        "S1": 8,
        "S2": 3,
        "S3": 3,
        "S4": 7,
        "S5": 0,
        "uncategorized": 272
    },
    "books": 0,
    "ipr": 2
}
```

Multiple authors can also be retrieved at once:

```
author_ids = 5975467, 6019743
author = sinta.author(author_id)
```

The output is a list of author dictionaries.

- ### `author_researches()`

Retrieves an author's researches. For example:

```
author_id = 6005015
researches = sinta.author_researches(author_id)

print(researches[:2])
```

Output:

```
[
    {
        "title": "Monitoring Kestabilan Transient dengan Mempertimbangkan Parameter Sudut Rotor, Frekuensi, dan Tegangan Berbasis Computational Intelligence",
        "scheme": "Penelitian Penugasan ( WCR )",
        "source": "Simlitabmas",
        "members": [
            "Mauridhi Hery Purnomo",
            "Ardyono Priyadi",
            "Vita Lystianingrum B P"
        ],
        "application_year": 2020,
        "event_year": 2021,
        "fund": 118488700,
        "field": "Energi",
        "sponsor": "Ristekdikti"
    },
    {
        "title": "Intelligent Teledermatology System untuk Smart Hospital",
        "scheme": "Penelitian Penugasan ( KRU-PT )",
        "source": "Simlitabmas",
        "members": [
            "I Ketut Eddy Purnama",
            "Anak Agung Putri Ratna",
            "Ingrid Nurtanio",
            "Afif Nurul Hidayati",
            "Reza Fuad Rachmadi",
            "Mauridhi Hery Purnomo",
            "Supeno Mardi Susiki Nugroho"
        ],
        "application_year": 2020,
        "event_year": 2021,
        "fund": 436800000,
        "field": "Kesehatan",
        "sponsor": "Ristekdikti"
    }
]
```

- ### `author_scholar_docs()`

Retrieves an author's Google Scholar items. For example:

```
author_id = 6005015
scholar_docs = sinta.author_scholar_docs(author_id)

print(scholar_docs[:2])
```

Output:

```
[
    {
        "title": "Konsep Pengolahan Citra Digital dan Ekstraksi Fitur",
        "url": "https://scholar.google.com/scholar?oi=bibs&cluster=11975243569176755366&btnI=1&hl=en",
        "publisher": "Yogyakarta: Graha Ilmu, 2010",
        "year": 2010,
        "citations": 0
    },
    {
        "title": "Supervised Neural Networks dan Aplikasinya",
        "url": "https://scholar.google.com/scholar?oi=bibs&cluster=4803627219094543302&btnI=1&hl=en",
        "publisher": "Yogyakarta: Graha Ilmu; ISBN:978-979-756-123-9 1 (2006), 176",
        "year": 2006,
        "citations": 0
    }
]
```

You can also specify the minimum and maximum year. For example:

```
author_id = 6005015
scholar = sinta.author_scholar_docs(author_id, min_year=2017, max_year=2020)
```

- ### `author_scopus_docs()`

Retrieves an author's Scopus documents. For example:

```
author_id = 6005015
scopus = sinta.author_scopus_docs(author_id)

print(scopus[:2])
```

Output:

```
[
    {
        "title": "Adaptive modified firefly algorithm for optimal coordination of overcurrent relays",
        "url": "https://www.scopus.com/record/display.uri?eid=2-s2.0-85026658931&origin=resultslist",
        "publisher": "IET Generation, Transmission and Distribution",
        "date": "2017-07-13",
        "type": "Journal",
        "quartile": 1,
        "citations": 77
    },
    {
        "title": "Controlling chaos and voltage collapse using an ANFIS-based composite controller-static var compensator in power systems",
        "url": "https://www.scopus.com/record/display.uri?eid=2-s2.0-84869223917&origin=resultslist",
        "publisher": "International Journal of Electrical Power and Energy Systems",
        "date": "2013-03-01",
        "type": "Journal",
        "quartile": 1,
        "citations": 62
    }
]
```

You can also specify the minimum and maximum date. The date must be in "yyyy-mm-dd" format. For example:

```
author_id = 6005015
scopus = sinta.author_scopus_docs(author_id, min_date='2015-01-01', max_date='2019-12-31')
```

- ### `author_scopus_journal_docs()`

Retrieves an author's Scopus journal documents. For example:

```
author_id = 6005015
scopus = sinta.author_scopus_journal_docs(author_id)
```

- ### `author_scopus_conference_docs()`

Retrieves an author's Scopus conference documents. For example:

```
author_id = 6005015
scopus = sinta.author_scopus_conference_docs(author_id)
```

- ### `author_wos_docs()`

Retrieves an author's Web of Science documents. For example:

```
author_id = 6005015
wos = sinta.author_wos_docs(author_id)

print(wos[:2])
```

Output:

```
[
    {
        "title": "Adaptive B-spline neural network-based vector control for a grid side converter in wind turbine-DFIG systems",
        "publisher": "IEEJ TRANSACTIONS ON ELECTRICAL AND ELECTRONIC ENGINEERING",
        "issn": "1931-4973",
        "doi": "-",
        "uid": "WOS:000362748500009"
    },
    {
        "title": "ARIMA Modeling of Tropical Rain Attenuation on a Short 28-GHz Terrestrial Link",
        "publisher": "IEEE ANTENNAS AND WIRELESS PROPAGATION LETTERS",
        "issn": "1536-1225",
        "doi": "10.1109/LAWP.2010.2046130",
        "uid": "WOS:000276520900002"
    }
]
```

- ### `author_comm_services()`

Retrieves an author's community service items. For example:

```
author_id = 5996278
comm_svc = sinta.author_comm_services(author_id)

print(comm_svc)
```

Output:

```
[
    {
        "title": "IbM Pembelajaran Elektronik Untuk SMK",
        "scheme": "Pengabdian Kepada Masyarakat Kompetitif Nasional ( PKM )",
        "source": "Simlitabmas",
        "members": [
            "Candra Dewi",
            "Adharul Muttaqin",
            "Achmad Basuki"
        ],
        "application_year": 2015,
        "event_year": 2016,
        "fund": 50000000,
        "field": "",
        "sponsor": "Ristekdikti"
    }
]
```

- ### `author_ipr()`

Retrieves an author's intellectual property right (IPR) items. For example:

```
author_id = 5996278
ipr = sinta.author_ipr(author_id)

print(ipr)
```

Output:

```
[
    {
        "id": "EC00202016549",
        "title": "Panduan Pembelajaran Daring Saat Kondisi Darurat COVID-19",
        "category": "paten",
        "year": "2020",
        "holder": "Universitas Brawijaya"
    }
]
```

- ### `dept_authors()`

Retrieves a list of authors associated with a department. Department ID and affiliation ID must be specified. The
output structure is different from that given by the `author()` function. This function retrieves only the ID and name
of each author. For example:

```
dept_id = 55001
affil_id = 417
authors = sinta.dept_authors(dept_id, affil_id)

print(authors)
```

Output:

```
[
    {
        "id": "29555",
        "name": "Riyanarto Sarno"
    },
    {
        "id": "6023328",
        "name": "Nanik Suciati"
    },
    {
        "id": "5975467",
        "name": "Agus Zainal Arifin"
    },
    {
        "id": "5993318",
        "name": "Handayani Tjandrasa"
    },
    {
        "id": "5993763",
        "name": "Joko Lianto Buliali"
    },
    {
        "id": "5995823",
        "name": "Supeno Djanali"
    }
]
```

Authors associated with multiple departments can also be retrieved at once:

```
dept_id = 55001, 90243
affil_id = 417
authors = sinta.dept_authors(dept_id, affil_id)
```

Note that the output is "flat", i.e. the authors from different departments are put into the same level.

- ### `dept_researches()`

Retrieves researches conducted by authors associated with some department(s). The affiliation ID must specified as well.
For example:

```
dept_id = 55001
affil_id = 417
researches = sinta.dept_researches(dept_id, affil_id)
```

The output format is the same as that given by the `author_researches()` function.
Multiple department ID's can be specified as long as they belong to the same affiliation. For example:

```
dept_id = 55001, 90243, 20001
affil_id = 417
researches = sinta.dept_researches(dept_id, affil_id)
```

- ### `dept_scholar_docs()`

Retrieves all Google Scholar documents written by authors in a department. For example:

```
dept_id = 55001
affil_id = 404
scholar_docs = sinta.dept_scholar_docs(dept_id, affil_id)

print(scholar_docs[0])
```

Output:

```
[
    {
        "id": "5977641",
        "name": "Wayan Firdaus Mahmudy",
        "docs": [
            {
                "title": "Algoritma Evolusi",
                "url": "https://scholar.google.com/scholar?oi=bibs&cluster=14954803897077959851,3266829010641986629&btnI=1&hl=en",
                "publisher": "Universitas Brawijaya. Malang",
                "year": 2013,
                "citations": 127
            },
            {
                "title": "Penerapan algoritma genetika pada sistem rekomendasi wisata kuliner",
                "url": "https://scholar.google.com/scholar?oi=bibs&cluster=10533163477803658267&btnI=1&hl=en",
                "publisher": "Kursor 5 (4), 205-211",
                "year": 2010,
                "citations": 63
            }
        ]
    },
    {
        "id": "5992836",
        "name": "Ahmad Afif Supianto",
        "docs": [
            {
                "title": "Rancang Bangun Aplikasi Antrian Poliklinik Berbasis Mobile",
                "url": "https://scholar.google.com/scholar?oi=bibs&cluster=4109969969855887623&btnI=1&hl=en",
                "publisher": "J. Teknol. Inf. dan Ilmu Komput 5 (3)",
                "year": 2018,
                "citations": 27
            },
            {
                "title": "Perbandingan Teknik Klasifikasi Dalam Data Mining Untuk Bank Direct Marketing",
                "url": "https://scholar.google.com/scholar?oi=bibs&cluster=10735231418349323236&btnI=1&hl=en",
                "publisher": "Jurnal Teknologi Informasi dan Ilmu Komputer 5 (5), 567-576",
                "year": 2018,
                "citations": 26
            }
        ]
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

For XML output, there are two library options which can be specified in the `xml_library` argument. These libraries give
different output formats. The options are:

- `dicttoxml` (default)
- `dict2xml`

Please note that the output is not wrapped in a root element. For example:

```
author = sinta.author(id, output_format='xml', xml_library='dict2xml')
```

Output:

```
<affiliation>
  <id>417</id>
  <name>Institut Teknologi Sepuluh Nopember</name>
  <url>http://sinta.ristekbrin.go.id/affiliations/detail/?id=417&amp;view=overview</url>
</affiliation>
<areas>computer vision</areas>
<areas>image processing</areas>
<areas>information retrieval</areas>
<areas>medical imaging</areas>
<areas>machine learning</areas>
<books>0</books>
<department>Teknik Informatika</department>
<id>5975467</id>
<ipr>2</ipr>
<name>AGUS ZAINAL ARIFIN</name>
<rank>
  <_3_years_affiliation>30</_3_years_affiliation>
  <_3_years_national>1099</_3_years_national>
  <affiliation>32</affiliation>
  <national>723</national>
</rank>
<scholar>
  <citations>1444</citations>
  <documents>294</documents>
  <g-index>31</g-index>
  <h-index>16</h-index>
  <i10-index>36</i10-index>
</scholar>
<scopus>
  <Q1>6</Q1>
  <Q2>12</Q2>
  <Q3>13</Q3>
  <Q4>3</Q4>
  <articles>39</articles>
  <citations>469</citations>
  <conferences>30</conferences>
  <documents>69</documents>
  <g-index>1</g-index>
  <h-index>10</h-index>
  <i10-index>10</i10-index>
  <others>0</others>
  <undefined>35</undefined>
</scopus>
<score>
  <_3_years>3.13</_3_years>
  <_3_years_v2>1377.5</_3_years_v2>
  <overall>48.1</overall>
  <overall_v2>4726.0</overall_v2>
</score>
<sinta>
  <S0>1</S0>
  <S1>8</S1>
  <S2>3</S2>
  <S3>3</S3>
  <S4>7</S4>
  <S5>0</S5>
  <uncategorized>272</uncategorized>
</sinta>
<url>https://sinta.kemdikbud.go.id/authors/detail?id=5975467&amp;view=overview</url>
<wos>
  <citations>None</citations>
  <documents>1</documents>
  <g-index>None</g-index>
  <h-index>None</h-index>
  <i10-index>None</i10-index>
</wos>
```

If you want the XML output to be pretty-printed, you need to choose `dict2xml` instead of `xmltodict` since the latter
does not produce pretty-printed XML output. By pretty-printing, the output is wrapped in a root element. For example:

```
author_id = '5975467'
author = sinta.author(author_id, output_format='xml', xml_library='dict2xml', pretty_print=True)

print(author)
```

Output:

```
<author>
    <affiliation>
        <id>417</id>
        <name>Institut Teknologi Sepuluh Nopember</name>
        <url>http://sinta.ristekbrin.go.id/affiliations/detail/?id=417&amp;view=overview</url>
    </affiliation>
    <areas>computer vision</areas>
    <areas>image processing</areas>
    <areas>information retrieval</areas>
    <areas>medical imaging</areas>
    <areas>machine learning</areas>
    <books>0</books>
    <department>Teknik Informatika</department>
    <id>5975467</id>
    <ipr>2</ipr>
    <name>AGUS ZAINAL ARIFIN</name>
    <rank>
        <_3_years_affiliation>30</_3_years_affiliation>
        <_3_years_national>1099</_3_years_national>
        <affiliation>32</affiliation>
        <national>723</national>
    </rank>
    <scholar>
        <citations>1444</citations>
        <documents>294</documents>
        <g-index>31</g-index>
        <h-index>16</h-index>
        <i10-index>36</i10-index>
    </scholar>
    <scopus>
        <Q1>6</Q1>
        <Q2>12</Q2>
        <Q3>13</Q3>
        <Q4>3</Q4>
        <articles>39</articles>
        <citations>469</citations>
        <conferences>30</conferences>
        <documents>69</documents>
        <g-index>1</g-index>
        <h-index>10</h-index>
        <i10-index>10</i10-index>
        <others>0</others>
        <undefined>35</undefined>
    </scopus>
    <score>
        <_3_years>3.13</_3_years>
        <_3_years_v2>1377.5</_3_years_v2>
        <overall>48.1</overall>
        <overall_v2>4726.0</overall_v2>
    </score>
    <sinta>
        <S0>1</S0>
        <S1>8</S1>
        <S2>3</S2>
        <S3>3</S3>
        <S4>7</S4>
        <S5>0</S5>
        <uncategorized>272</uncategorized>
    </sinta>
    <url>https://sinta.kemdikbud.go.id/authors/detail?id=5975467&amp;view=overview</url>
    <wos>
        <citations>None</citations>
        <documents>1</documents>
        <g-index>None</g-index>
        <h-index>None</h-index>
        <i10-index>None</i10-index>
    </wos>
</author>
```

### Todo

- Other output formats: CSV.
- `find_affil(keyword)` function.
- `affil_depts(affil_id)` function.
- `dept(dept_id)` function.
- `find_dept(keyword)` function.
- `dept_scholar_citations_count(dept_id)` function.
- `dept_scopus_citations_count(dept_id)` function.
- `dept_wos_citations_count(dept_id)` function.
- `affil_citations_count(author_id)` function.
- Sinta 3.
