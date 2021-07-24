import re

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import ResultSet
from progress.bar import Bar
from requests.models import Response


def getHTML(letter: str, page: str = "1") -> BeautifulSoup:
    resp: Response = requests.get(
        url="https://www.merriam-webster.com/browse/dictionary/" + letter + "/" + page
    ).text
    return BeautifulSoup(markup=resp, features="lxml")


def getNumberOfPages(html: BeautifulSoup) -> int:
    numberOfPagesText: str = html.find(name="span", attrs={"class": "counters"}).text
    try:
        pages: int = int(re.findall("[^\D+]\d+", numberOfPagesText)[-1])
    except IndexError:
        pages: int = int(re.findall("\d", numberOfPagesText)[-1])
    return pages


def getWords(html: BeautifulSoup) -> list:
    words: list = []
    wordsDiv: Tag = html.find(name="div", attrs={"class": "entries"})
    wordsList: ResultSet = wordsDiv.find_all(name="a")

    word: str
    for word in wordsList:
        words.append(word.text)
    return words


if __name__ == "__main__":
    words: list = []
    letterList: list = ["0"]
    pageCount: list = []

    unicodeChar: int
    for unicodeChar in range(97, 123):
        letterList.append(chr(unicodeChar).lower())

    with Bar("Getting page numbers for dictionary keys... ", max=27) as bar:

        letter: str
        for letter in letterList:
            firstPage: BeautifulSoup = getHTML(letter=letter)
            pageCount: int = getNumberOfPages(firstPage)
            pageCount.append(pageCount)
            bar.next()

    mwDict = dict(zip(letterList, pageCount))

    key: str
    for key in mwDict.keys():
        with Bar(
            "Getting words listed under the dictionary index: " + key + "... ",
            max=mwDict[key],
        ) as bar:
            page: int
            for page in range(mwDict[key]):
                pageString: str = str(page + 1)
                html: BeautifulSoup = getHTML(letter=key, page=pageString)
                words += getWords(html=html)
                mwDict[key] = len(words)
                bar.next()

    with open("output/MerriamWebster_WordList.txt", "w") as wordList:
        word: str
        for word in words:
            wordList.write(word + "\n")
        print("Wrote word list to file")
        wordList.close()
