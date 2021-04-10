import requests
from bs4 import BeautifulSoup


class WordList:
    def __init__(self) -> None:
        self.merriamWebsterURL = "https://www.merriam-webster.com/browse/dictionary/"

    def getHTML(self, url: str) -> BeautifulSoup:
        resp = requests.get(url=url).text
        return BeautifulSoup(markup=resp, features="lxml")

    def program(self) -> bool:
        return False


w = WordList()
print(type(w.getHTML(w.merriamWebsterURL)))
