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

Use the supplied `Dockerfile` to build and run the image:

```bash
$ docker build -t isbn_api .
$ docker run --rm --name isbn_api --port 8000:8000 localhost/isbn_api
```

The server will be accessible at port `8000`.

Note: tested using rootless containers, you might need to `sudo` the commands
if using Docker.

### Via docker-compose

The `docker-compose.yaml` file provides a simple way to spin up the ISBN REST
API and an Nginx instance.

This way you have an Nginx caching the queries, as well as load balancing the
requests between two API instances: `main` and `fallback`. The port to query
the functionality is `8080`, instead of `8000`.

To use it:

```bash
$ docker-compose up --detach
```

#### Caching

Nginx is configured to cache only the `/books/` endpoint. You can check if a
request was cached by the `X-Proxy-Cache` response header:

```bash
$ curl 192.168.1.13:8080/ -D -
HTTP/1.1 200 OK
Server: nginx/1.23.3
Date: Fri, 06 Jan 2023 14:03:08 GMT
Content-Type: application/json
Content-Length: 36
Connection: keep-alive

{"message":"Hello from server main"}

$ curl 192.168.1.13:8080/books/1503222683 -D -
HTTP/1.1 200 OK
Server: nginx/1.23.3
Date: Fri, 06 Jan 2023 14:03:14 GMT
Content-Type: application/json
Content-Length: 188
Connection: keep-alive
X-Proxy-Cache: MISS

{"title":"Alice's Adventures in Wonderland","isbn10":["1503222683"],"isbn13":["9781503222687"],"authors":["Lewis Carroll"],"cover_url":"https://covers.openlibrary.org/b/id/10476757-M.jpg"}

$ curl 192.168.1.13:8080/books/1503222683 -D -
HTTP/1.1 200 OK
Server: nginx/1.23.3
Date: Fri, 06 Jan 2023 14:03:16 GMT
Content-Type: application/json
Content-Length: 188
Connection: keep-alive
X-Proxy-Cache: HIT

{"title":"Alice's Adventures in Wonderland","isbn10":["1503222683"],"isbn13":["9781503222687"],"authors":["Lewis Carroll"],"cover_url":"https://covers.openlibrary.org/b/id/10476757-M.jpg"}
```

#### Load balancing

Load balancing is done in a round-robing fashion, with the `main` instance
handling 60% of the requests:

```bash
$ for i in {1..20}; do curl 192.168.1.13:8080/ ; echo; done
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
{"message":"Hello from server fallback"}
{"message":"Hello from server main"}
```

## Tests

To run the tests for the API:

```bash
$ hatch run cov
======================= test session starts ======================
platform linux -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/projects/isbn-api
plugins: anyio-3.6.2, cov-4.0.0
collected 9 items

tests/test_config.py .                                      [ 11%]
tests/test_main.py ........                                 [100%]

-------- coverage: platform linux, python 3.10.8-final-0 ---------
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
isbn_api/__init__.py       0      0      0      0   100%
isbn_api/config.py         3      0      0      0   100%
isbn_api/main.py          33      0      4      0   100%
tests/test_config.py       5      0      0      0   100%
tests/test_main.py        39      0      0      0   100%
------------------------------------------------------------------
TOTAL                     80      0      4      0   100%

======================== 9 passed in 2.28s =======================
```

## License

`isbn-api` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
