import re

import requests
from bs4 import BeautifulSoup


class WordList:
    def __init__(self) -> None:
        self.merriamWebsterURL = "https://www.merriam-webster.com/browse/dictionary/"

    def getHTML(self, url: str) -> BeautifulSoup:
        resp = requests.get(url=url).text
        return BeautifulSoup(markup=resp, features="lxml")

    def parseHTML(self, html: BeautifulSoup) -> tuple:
        def getNumberOfPages() -> int:
            numberOfPagesText = html.find(name="span", attrs={"class": "counters"})
            print(numberOfPagesText.text)

        wordSet = set()
        getNumberOfPages()

    def program(self) -> bool:
        return False


w = WordList()
h = w.getHTML(w.merriamWebsterURL)
p = w.parseHTML(h)
