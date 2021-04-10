import re

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import ResultSet
from progress.bar import Bar
from progress.spinner import MoonSpinner


class WordList:
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

    with MoonSpinner("Creating Char List... ") as spinner:
        for unicodeChar in range(97, 123):
            mwLetterList.append(chr(unicodeChar).lower())
            spinner.next()

    print()

    mw = WordList()

    with Bar("Getting Page Numbers for Dictionary Indicies... ", max=27) as bar:
        for letter in mwLetterList:
            firstPage = mw.getHTML(letter=letter)
            pageCount = mw.getNumberOfPages(firstPage)
            mwPageCount.append(pageCount)
            bar.next()

    mwDict = dict(zip(mwLetterList, mwPageCount))

    print()

    for key in mwDict.keys():
        with Bar(
            "Getting Words Under the Dictionary Index: " + key + "... ",
            max=mwDict[key],
        ) as bar:
            for page in range(mwDict[key]):
                pageString = str(page + 1)
                html = mw.getHTML(letter=key, page=pageString)
                words += mw.getWords(html=html)
                mwDict[key] = len(words)
                bar.next()

    print()

    with open("MerriamWebster_WordList.txt", "w") as wordList:
        for word in words:
            wordList.write(word + "\n")
        print("Wrote word list to file")
        wordList.close()
    return True


if __name__ == "__main__":
    program()
