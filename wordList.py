import re

import requests
from bs4 import BeautifulSoup, Tag


class WordList:
    def __init__(self) -> None:
        self.merriamWebsterURL = "https://www.merriam-webster.com/browse/dictionary/"

    def getHTML(self, letter: str, page: str) -> BeautifulSoup:
        resp = requests.get(url=self.merriamWebsterURL + letter + "/" + page).text
        return BeautifulSoup(markup=resp, features="lxml")

    def parseHTML(self, html: BeautifulSoup) -> tuple:
        def _getNumberOfPages() -> int:
            numberOfPagesText = html.find(name="span", attrs={"class": "counters"}).text
            pages = int(re.findall("[^\D+]\d+", numberOfPagesText)[-1])
            return pages

        def _getWords() -> set():
            words = set()
            wordsDiv: Tag = html.find(name="div", attrs={"class": "entries"})
            wordsList = wordsDiv.find_all(name="a")
            for word in wordsList:
                words.add(word.text)
            return words

        return (_getNumberOfPages(), _getWords())

    def program(self) -> bool:
        return False


w = WordList()
h = w.getHTML("a", "1")
p = w.parseHTML(h)
