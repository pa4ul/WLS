import click
import requests
import re
from bs4 import BeautifulSoup
import json


words_from_different_urls = {}


def get_html_of(url):
    resp = requests.get(url)

    # not working properly
    if resp.status_code != 200:
        print(
            f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)

    return resp.content.decode()


def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count


def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)


def get_top_words_from(all_words, min_length):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)


def spyder_specific_url(url, length, how_much_words):
    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, length)

    for i in range(how_much_words):
        print(top_words[i][0])
        top_words_general(top_words[i][0])


def top_words_general(word):
    global words_from_different_urls

    if word not in words_from_different_urls:
        words_from_different_urls[word] = 1
    else:
        current_count = words_from_different_urls.get(word)
        words_from_different_urls[word] = current_count + 1


def read_wfuzz_file(src):
    url_list = []

    with open(src) as file:
        json_data = json.load(file)

    for i in json_data:
        if i['url'] not in url_list:
            url_list.append(i['url'])

    return url_list


@click.command()
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--source', '-src', prompt='Specify the JSON file from wfuzz', help='Specify the JSON file from wfuzz')
@click.option('--size', '-s', prompt='How many words should be generated?', help='The most popular words will be written into the wordlist. Here you have to define how many words you want to have in the wordlist.')
def main(length, source, size):

    url_list = read_wfuzz_file(source)
    for url in url_list:
        print("==============================")
        spyder_specific_url(url, length, int(size))
    print("===========TOP WORDS==============")
    for i in words_from_different_urls:
        print(i) ##CONTINUE HERE (WORDS-FROM-DIFFERENT-URLS) check the number how often a word occurs

if __name__ == '__main__':
    main()
