import json
from pathlib import Path
from typing import Any

from src.models import Author, Quote
import connect


def read_json_file(file_name: str, encoding: str = 'utf-8') -> Any:
    """Read data from json-file, and return data."""
    file_path = Path('..', 'json', file_name)
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
    return data


def upload_authors_to_the_database() -> None:
    """Upload authors from json-file to database."""
    authors = read_json_file('authors.json')
    [Author(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
        ).save()
        for author in authors]


def upload_quotes_to_the_database() -> None:
    """Upload quotes from json-file to database."""
    quotes = read_json_file('quotes.json')
    for quote in quotes:
        author = Author.objects(fullname=quote['author']).first()
        if author.id:
            Quote(
                tags=quote['tags'],
                author=author.id,
                quote=quote['quote']
                ).save()

        else:
            print(f'Author "{quote["author"]}" is unknown!')


if __name__ == "__main__":
    if not Quote.objects():
        upload_authors_to_the_database()
        upload_quotes_to_the_database()
