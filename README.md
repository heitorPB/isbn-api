# ISBN API

Query books' information via their ISBN.

-----

**Table of Contents**

- [Usage](#usage)
- [Running the server](#running-the-server)
- [License](#license)

## Usage

This API has two endpoints:

- `/` (GET):
  ```bash
  $ curl localhost:8000/
  {"message":"Hello, you are currently working with server 1"}
  ```
- `/books/<ISBN>` (GET):
  ```bash
  $ curl localhost:8000/books/9780140328721 | jq
  {
  "title": "Fantastic Mr. Fox",
  "isbn10": [
    "0140328726"
  ],
  "isbn13": [
    "9780140328721"
  ],
  "authors": [
    "Roald Dahl"
  ],
  "cover_url": "https://covers.openlibrary.org/b/id/8739161-M.jpg"
  }
  ```

This system also has interactive documentation at
[`/doc`](http://localhost:8000/doc) and an alternative one at
[`/redoc`](http://localhost:8000/doc) (this is not interactive).

You can check the OpenAPI specification for this system at
[/openapi.json](http://localhost:8000/openapi.json)

## Running the server

Some ways to have the server running:

### Run the server directly

Install the dependencies and run the server:

- Using [hatch](https://hatch.pypa.io/), the Python package manager:
  ```bash
  $ hatch serve
  ```
- Directly via Python and a virtual environment:
  ```bash
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ pip install .
  $ uvicorn isbn_api.main:app --host 0.0.0.0
  ```

The server will be listening on port `8000`.

### Via Docker

### Via docker-compose

This way you have an Nginx caching the queries, as well as load balancing the
requests between two instances. The port to query the functionality is `80`,
instead of `8000`.

## Tests

To run the tests for the API:

```bash
$ hatch run cov
======================= test session starts =======================
platform linux -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/projects/isbn-api
plugins: anyio-3.6.2, cov-4.0.0
collected 8 items

tests/test_main.py ........                                 [100%]

---------- coverage: platform linux, python 3.10.8-final-0 -----------
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
isbn_api/__init__.py       0      0      0      0   100%
isbn_api/main.py          29      0      4      0   100%
tests/__init__.py          0      0      0      0   100%
tests/test_main.py        35      0      0      0   100%
------------------------------------------------------------------
TOTAL                     64      0      4      0   100%


======================== 8 passed in 2.30s ========================
```

## License

`isbn-api` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
