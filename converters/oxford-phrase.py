import sys
from bs4 import BeautifulSoup

from converters import oxford


def parse(item: BeautifulSoup) -> oxford.Entry:
    word = item.get("data-hw")
    level = item.get("data-oxford_phrase_list")

    definition_el = item.find("a")
    definition_url = definition_el.get("href") if definition_el else None
    definition_url = oxford.BASE_URL + definition_url if definition_url else None

    voice_el = item.find("div", class_="pron-us")
    voice_url = voice_el.get("data-src-ogg") if voice_el else None
    voice_url = oxford.BASE_URL + voice_url if voice_url else None

    return oxford.Entry(word, level, pos=None, definition_url=definition_url, voice_url=voice_url)


if __name__ == "__main__":
    oxford.to_csv(sys.argv[1], sys.argv[2], parse)
