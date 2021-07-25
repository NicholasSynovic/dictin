import re
from json import dumps

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import ResultSet
from progress.bar import PixelBar
from requests.models import Response


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
        encodedWord: str = word.text.encode("UTF-8")
        words.append(encodedWord.decode("UTF-8"))
    return words


def getWordType(html: BeautifulSoup) -> list:
    wtList: list = []
    wtResultSet: ResultSet = html.find_all(
        name="a", attrs={"class": "important-blue-link"}
    )

    wtTag: Tag
    for wtTag in wtResultSet:
        wtList.append(wtTag.text)
    return wtList


def writeToJSON(filename: str, store: dict) -> bool:
    with open(file=filename, mode="w", encoding="utf-8") as wordFile:
        wordFile.write(dumps(obj=store, ensure_ascii=False))
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
        data: dict = {}

        data["letter"] = key
        data["numberOfWords"] = 0
        data["urls"] = {}

        with PixelBar(
            f"Getting words listed under the dictionary index: {key}... ",
            max=store[key]["wordPageCount"],
        ) as pb:
            page: int
            for page in range(store[key]["wordPageCount"]):
                pageString: str = str(page + 1)

                url: str = f"https://www.merriam-webster.com/browse/dictionary/{key}/{pageString}"

                html: BeautifulSoup = getHTML(url=url)
                words += getWords(html=html)

                data["numberOfWords"] += len(words)

                data["urls"][url] = {"words": []}

                for index in range(len(words)):
                    wordURL = (
                        f"https://www.merriam-webster.com/dictionary/{words[index]}"
                    ).replace(" ", "+")

                    # html = getHTML(url=wordURL)

                    data["urls"][url]["words"].append(
                        {
                            words[index]: [
                                wordURL,
                            ]
                        }
                    )

                pb.next()

        writeToJSON(filename=f"output/{key}.json", store=data)
