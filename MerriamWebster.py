import re

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import ResultSet
from progress.bar import Bar
from progress.spinner import MoonSpinner
from requests.models import Response


class WordList:
    def __init__(self) -> None:
        self.merriamWebsterURL: str = (
            "https://www.merriam-webster.com/browse/dictionary/"
        )
        self.currentURL: str = ""

    def getHTML(self, letter: str, page: str = "1") -> BeautifulSoup:
        self.currentURL = self.merriamWebsterURL + letter + "/" + page
        resp: Response = requests.get(url=self.currentURL).text
        return BeautifulSoup(markup=resp, features="lxml")

    def getNumberOfPages(self, html: BeautifulSoup) -> int:
        numberOfPagesText: str = html.find(
            name="span", attrs={"class": "counters"}
        ).text
        try:
            pages: int = int(re.findall("[^\D+]\d+", numberOfPagesText)[-1])
        except IndexError:
            pages: int = int(re.findall("\d", numberOfPagesText)[-1])
        return pages

    def getWords(self, html: BeautifulSoup) -> list:
        words: list = []
        wordsDiv: Tag = html.find(name="div", attrs={"class": "entries"})
        wordsList: ResultSet = wordsDiv.find_all(name="a")

        word: str
        for word in wordsList:
            words.append(word.text)
        return words


if __name__ == "__main__":
    words: list = []
    mwLetterList: list = ["0"]
    mwPageCount: list = []

    unicodeChar: int
    for unicodeChar in range(97, 123):
        mwLetterList.append(chr(unicodeChar).lower())

    mw: WordList = WordList()

    with Bar("Getting page numbers for dictionary keys... ", max=27) as bar:

        letter: str
        for letter in mwLetterList:
            firstPage: BeautifulSoup = mw.getHTML(letter=letter)
            pageCount: int = mw.getNumberOfPages(firstPage)
            mwPageCount.append(pageCount)
            bar.next()

    mwDict = dict(zip(mwLetterList, mwPageCount))

    key: str
    for key in mwDict.keys():
        with Bar(
            "Getting words listed under the dictionary index: " + key + "... ",
            max=mwDict[key],
        ) as bar:
            page: int
            for page in range(mwDict[key]):
                pageString: str = str(page + 1)
                html: BeautifulSoup = mw.getHTML(letter=key, page=pageString)
                words += mw.getWords(html=html)
                mwDict[key] = len(words)
                bar.next()

    with open("output/MerriamWebster_WordList.txt", "w") as wordList:
        word: str
        for word in words:
            wordList.write(word + "\n")
        print("Wrote word list to file")
        wordList.close()
