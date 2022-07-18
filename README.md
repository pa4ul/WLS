<h1 align="center">
	Wordlist Spider
</h1>

<h3 align="center">
	WLS spiders multiple URLs and returns a list of words which can then be used for password bruteforcing.
</h3>

<p align="center">
	<img src="https://img.shields.io/github/license/pa4ul/WLS?color=green"/>
	<img src="https://img.shields.io/github/repo-size/pa4ul/WLS?color=green"/>
	<img src="https://img.shields.io/github/last-commit/pa4ul/WLS?color=green"/>
</p>

<h4 align="center">
	Status: 🚧 In Construction
</h4>

<p align="center">
	<a href="#about">About</a> •
	<a href="#tech-stack">Tech Stack</a> •
	<a href="#installation">Installation</a> •
	<a href="#usage">Usage</a> •
</p>

## About
WLS (Wordlist Spider) is a python programm that parses the *.json* output of *wfuzz* and then returns a list of the most used words from all these URLs together. 

The words can be filtered to a minimum length. You can also define with which *user agent* and how many of the most used words should be output. 

The generated wordlist can be stored in an extra file.

## Tech Stack
<img src="https://img.shields.io/badge/Python-05122A?style=flat&logo=python" alt="python Badge" height="25">&nbsp;

## Installation
To Install this project, follow the steps above:
```bash
# Installation
git clone https://github.com/pa4ul/WLS.git
cd WLS

```

## Usage
To use this project, follow the steps above:
```bash
# Run the application
python3 wls.py [OPTIONS]


# Getting help
python3 wls.py --help

Options:
  -l, --length INTEGER   Minimum word length (default: 0, no limit).
  -src, --source TEXT    Specify the JSON file from wfuzz
  -ua, --useragent TEXT  Specify the User-Agent to send. Default is "python-
                         requests/2.28.1"

  -o, --output TEXT      Write the output to the file.
  -s, --size TEXT        The most popular words will be written into the
                         wordlist. Here you have to define how many words you
                         want to have in the wordlist.

  --help                 Show this message and exit.


```

