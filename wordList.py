import re
from bs4.element import ResultSet

import requests
from bs4 import BeautifulSoup, Tag


class MerriamWebster:
    def __init__(self) -> None:
        self.merriamWebsterURL = "https://www.merriam-webster.com/browse/dictionary/"
        self.currentURL: str = ""

    def getHTML(self, letter: str, page: str = "1") -> BeautifulSoup:
        self.currentURL = self.merriamWebsterURL + letter + "/" + page
        resp = requests.get(url=self.currentURL).text
        return BeautifulSoup(markup=resp, features="lxml")

    def getNumberOfPages(self, html: BeautifulSoup) -> int:
        numberOfPagesText = html.find(name="span", attrs={"class": "counters"}).text
        try:
            pages = int(re.findall("[^\D+]\d+", numberOfPagesText)[-1])
        except IndexError:
            pages = int(re.findall("\d", numberOfPagesText)[-1])
        return pages

    def getWords(self, html: BeautifulSoup) -> list:
        words = []
        wordsDiv: Tag = html.find(name="div", attrs={"class": "entries"})
        wordsList: ResultSet = wordsDiv.find_all(name="a")
        for word in wordsList:
            words.append(word.text)
        return words


def program() -> bool:
    words = []
    mwLetterList = ["0"]
    mwPageCount = []

    for unicodeChar in range(97, 123):
        mwLetterList.append(chr(unicodeChar).lower())

    mw = MerriamWebster()

    for letter in mwLetterList:
        firstPage = mw.getHTML(letter=letter)
        pageCount = mw.getNumberOfPages(firstPage)
        mwPageCount.append(pageCount)

    mwDict = dict(zip(mwLetterList, mwPageCount))

    for key in mwDict.keys():
        for page in range(mwDict[key]):
            pageString = str(page + 1)
            html = mw.getHTML(letter=key, page=pageString)
            words += mw.getWords(html=html)


program()
