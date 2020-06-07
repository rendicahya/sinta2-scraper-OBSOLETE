# Sinta Scraper

Retrieve various information from Sinta (http://sinta.ristekbrin.go.id) via scraping.

## Installation
`pip install sinta-scraper`

## Usage

#### Import
`import sinta-scraper as sinta`

##### Get author information by Sinta ID
```
id = '5975467'
author = sinta.author(id)
```

#### Output
The output is of dictionary type.

#### Available Functions
- `author(sinta_id)`: gets an author's information. 
- `dept_authors(dept_id)`: gets authors associated with a department.
