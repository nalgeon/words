"""
Parse Oxford word lists from html to csv.
https://www.oxfordlearnersdictionaries.com/wordlists/

First save the list as html (only the li's inside the list ul).
Then run the tool:

    python3 -m converters.oxford-5k data/oxford-5k.html data/oxford-5k.csv
    python3 -m converters.oxford-opal data/oxford-opal.html data/oxford-opal.csv
    python3 -m converters.oxford-phrase data/oxford-phrase.html data/oxford-phrase.csv

After that, data/*.csv will contain lists in csv.
"""

import csv
import dataclasses
from typing import Iterator, Callable
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = "https://www.oxfordlearnersdictionaries.com"


@dataclasses.dataclass
class Entry:
    word: str
    level: str
    pos: str
    definition_url: str
    voice_url: str = None


def load_source(filename: str) -> BeautifulSoup:
    text = ""
    with open(filename) as file:
        text = file.read()
    return BeautifulSoup(text, "lxml")


def reader(soup: BeautifulSoup, parse_fn: Callable[[BeautifulSoup], Entry]) -> Iterator[Entry]:
    for item in soup.body:
        if not isinstance(item, Tag):
            continue
        # if item.get("class") == ["hidden"]:
        #     continue
        entry = parse_fn(item)
        yield entry


def writer(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        header = [field.name for field in dataclasses.fields(Entry)]
        writer.writerow(header)
        while True:
            row = yield
            writer.writerow(row)


def to_csv(in_filename: str, out_filename: str, parse_fn: Callable[[BeautifulSoup], Entry]):
    soup = load_source(in_filename)
    w = writer(out_filename)
    next(w)
    for entry in reader(soup, parse_fn):
        print(entry.word)
        w.send([entry.word, entry.level, entry.pos, entry.definition_url, entry.voice_url])
    w.close()
