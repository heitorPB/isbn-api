# ISBN API

Query books' information via their ISBN.

-----

**Table of Contents**

- [Usage](#usage)
- [Running the server](#running-the-server)
- [License](#license)

## Usage

This API has two endpoints:

- `/` (GET)
    TODO: add example of query and its output
- `/book/<ISBN>` (GET)
    TODO: add example of query and its output

As well as an interactive documentation at `/doc` and an alternative one at
`/redoc` (this is not interactive).

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

The server will be listening on port 8000.

### Via Docker

### Via docker-compose

## License

`isbn-api` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
