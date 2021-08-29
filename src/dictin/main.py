import re
from json import dumps, load
from os.path import exists

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import ResultSet
from requests.models import Response
from progress.bar import PixelBar


def getLetterPageCount(letter: str) -> int:
    url: str = f"https://www.merriam-webster.com/browse/dictionary/{letter}/1"

    html: BeautifulSoup = getHTML(url=url)

    numberOfPagesText: str = html.find(name="span", attrs={"class": "counters"}).text

    try:
        pages: int = int(re.findall("[^\D+]\d+", numberOfPagesText)[-1])
    except IndexError:
        pages: int = int(re.findall("\d", numberOfPagesText)[-1])
    return pages


def getHTML(url: str) -> BeautifulSoup:
    resp: Response = requests.get(url=url).text
    return BeautifulSoup(markup=resp, features="lxml")


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
    with open(file=filename, mode="w", encoding="utf-8") as jsonFile:
        jsonFile.write(dumps(obj=store, ensure_ascii=False))
        jsonFile.close()
    if exists(filename):
        print(f"Wrote word list to file: output/{filename}")
        return True
    return False


def loadJSON(filename: str) -> dict:
    data: dict
    with open(file=filename, mode="r") as jsonFile:
        data = load(fp=jsonFile)
        jsonFile.close()
    print(f"Load word list from file: output/{filename}")
    return data


def main() -> None:

    # This function is to large, lets break it up

    # Get all of the letters of the alphabet and the number of page indexes that they have
    temp: dict = {}
    with PixelBar("Getting page numbers for dictionary keys... ", max=27) as pb:
        unicodeLetter: chr
        i: int
        for i in range(96, 123):
            if i == 96:
                unicodeLetter = "0"
            else:
                unicodeLetter = chr(i)
            temp[unicodeLetter] = getLetterPageCount(unicodeLetter)
            pb.next()

    # For each letter return all of the words starting with that letter and write it to JSON
    letter: str
    for letter in temp.keys():

        data: dict = {}
        data["letter"] = letter
        data["indexURLs"] = {}

        with PixelBar(
            f"Getting words listed under the dictionary index: {letter}... ",
            max=temp[letter],
        ) as pb:
            i: int
            for i in range(temp[letter]):
                wordList: list
                indexURL: str = f"https://www.merriam-webster.com/browse/dictionary/{letter}/{i + 1}"

                html: BeautifulSoup = getHTML(url=indexURL)
                wordList = getWords(html=html)

                data["indexURLs"][indexURL] = {"numberOfWords": 0, "words": []}
                data["indexURLs"][indexURL]["numberOfWords"] = len(wordList)

                word: str
                for word in wordList:
                    data["indexURLs"][indexURL]["words"].append(
                        {
                            "word": word,
                            "type": [],
                            "definitions": [],
                            "wordURL": f"https://www.merriam-webster.com/dictionary/{word}".replace(
                                " ", "+"
                            ),
                        }
                    )
                pb.next()

        writeToJSON(filename=f"output/{letter}.json", store=data)

    # Load data from JSON file and get all of the word types associated with the words

    i: int
    unicodeLetter: chr
    for i in range(96, 123):
        if i == 96:
            unicodeLetter = "0"
        else:
            unicodeLetter = chr(i)

        jsonFile: dict = loadJSON(filename=f"output/{unicodeLetter}.json")

        wordList: list
        index: str
        for index in jsonFile["indexURLs"].keys():
            urlIndexData: dict = jsonFile["indexURLs"][index]

            word: dict
            for word in urlIndexData["words"]:
                wordTypeList: list = []

                wordHTML: BeautifulSoup = getHTML(url=word["wordURL"])

                wordTypeResultSet: ResultSet = wordHTML.find_all(
                    name="a", attrs={"class": "important-blue-link"}
                )

                # TODO: This for loop could be more efficent
                wordTypeTag: Tag
                for wordTypeTag in wordTypeResultSet:
                    wordTypeList.append(wordTypeTag.text)

                    try:
                        subType: str = wordTypeTag.find(
                            name="a", attrs={"class": "important-blue-link"}
                        ).text

                        wordTypeList.append(subType)
                    except AttributeError:
                        pass

                word["type"] = wordTypeList

        writeToJSON(filename=f"output/{unicodeLetter}.json", store=jsonFile)


if __name__ == "__main__":
    main()
