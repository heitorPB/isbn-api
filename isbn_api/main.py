# SPDX-FileCopyrightText: 2023-present Heitor Pascoal de Bittencourt <heitorpbittencourt@gmail.com>
#
# SPDX-License-Identifier: MIT

from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

from .__about__ import VERSION

DESCRIPTION = """Query book information."""

app = FastAPI(title="ISBN API",
              description=DESCRIPTION,
              version=VERSION,
              license_info={"name": "MIT",
                            "url": "https://opensource.org/licenses/MIT"},
             )

# TODO: get this config from the environment
SERVER_NAME = "1"

class Book(BaseModel):
    title: str
    isbn10: list[str]
    isbn13: list[str]
    authors: list[str]
    cover_url: str # TODO change type to url

class Message(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": f"Hello, you are currently working with server {SERVER_NAME}"}

@app.get("/books/{isbn}",
         response_model=Book,
         responses={404: {"model": Message}})
async def book(isbn: str = Path(title="ISBN of the book", min_length=10,
                                max_length=13, regex="^(\d{10}|\d{13})$")):
    url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    r = requests.get(url)

    if len(r.json()) == 0:
        return JSONResponse(status_code=404,
                            content={"message": f"ISBN {isbn} not found"})

    book_key = f"ISBN:{isbn}"
    book_data = r.json()[book_key]
    book = Book(
        title = book_data["title"],
        isbn10 = book_data["identifiers"]["isbn_10"],
        isbn13 = book_data["identifiers"]["isbn_13"],
        authors = [author["name"] for author in book_data["authors"]],
        cover_url = book_data["cover"]["medium"],
    )

    return book
