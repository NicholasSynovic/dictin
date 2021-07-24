import re

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import ResultSet
from progress.bar import PixelBar
from requests.models import Response

from json import dumps


def getHTML(url: str) -> BeautifulSoup:
    resp: Response = requests.get(url=url).text
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


def writeToJSON(filename: str, store: dict) -> bool:
    with open(filename, "w") as wordFile:
        wordFile.write(dumps(store))
        print(f"Wrote word list to file output/{filename}")
        wordFile.close()


if __name__ == "__main__":
    words: list = []
    letterList: list = ["0"]
    pageCount: list = []

    unicodeChar: int
    for unicodeChar in range(97, 123):
        letterList.append(chr(unicodeChar).lower())

    with PixelBar("Getting page numbers for dictionary keys... ", max=27) as pb:

        letter: str
        for letter in letterList:
            url: str = f"https://www.merriam-webster.com/browse/dictionary/{letter}/1"
            firstPage: BeautifulSoup = getHTML(url=url)
            pages: int = getNumberOfPages(firstPage)
            pageCount.append({"wordPageCount": pages})
            pb.next()

    store = dict(zip(letterList, pageCount))

    key: str
    for key in store.keys():

        store[key]["numberOfWords"] = 0
        store[key]["urls"] = {}

        with PixelBar(
            "Getting words listed under the dictionary index: " + key + "... ",
            max=store[key]["wordPageCount"],
        ) as pb:
            page: int
            for page in range(store[key]["wordPageCount"]):
                pageString: str = str(page + 1)

                url: str = f"https://www.merriam-webster.com/browse/dictionary/{key}/{pageString}"

                html: BeautifulSoup = getHTML(url=url)
                words += getWords(html=html)

                store[key]["urls"][url] = words
                store[key]["numberOfWords"] += len(words)

                pb.next()

        writeToJSON(filename=f"{key}.json", store=store[key])
