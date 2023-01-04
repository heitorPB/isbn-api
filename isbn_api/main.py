# SPDX-FileCopyrightText: 2023-present Heitor Pascoal de Bittencourt <heitorpbittencourt@gmail.com>
#
# SPDX-License-Identifier: MIT

from fastapi import FastAPI

from .__about__ import VERSION

description = """Query book information."""

app = FastAPI(title="ISBN API",
              description=description,
              version=VERSION,
              license_info={"name": "MIT",
                            "url": "https://opensource.org/licenses/MIT"},
             )

# TODO: get this config from the environment
SERVER_NAME = "1"

@app.get("/")
async def root():
    return {"message": f"Hello, you are currently working with server {SERVER_NAME}"}

@app.get("/book/{isbn}")
async def book(isbn: str):
    # preprocess input: replace dashes, strip, etc
    # request openlibrary.org
    # parse output and return
    return {"ISBN": isbn}
