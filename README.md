# Dictionary Generator

> A program meant to generate word and definition lists derived from online dictionaries.

## Table of Contents

- [Dictionary Generator](#dictionary-generator)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [How to Execute](#how-to-execute)
  - [TODO](#todo)

## About

- Is this a web scraping program? **Yes**
- Does this program break online dictionary TOS? **Probably**

This application goes to online dictionaries (currently Merriam Webster) and scrapes their directory of words to generate word lists and their definitions.

## How to Execute

1. In a terminal execute: `docker build -t dictionaryGenerator .`
2. In a terminal execute: `docker run -v "$(pwd)":DictionaryGenerator-Output dictionaryGenerator`

## TODO

1. Improve program execution
2. Create release files of the word lists and dictionary files
3. Automate release files
4. Collect definitions
5. Create log file containing the amount of words under a given letter
6. Add multithreading
7. Add more dictionaries
