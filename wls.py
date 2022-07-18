import click
import requests
import re
from bs4 import BeautifulSoup
import json

words_from_different_urls = {}
user_agent = 'python-requests/2.28.1'


def get_html_of(url):
    str_user_agent = str(user_agent)
    header = {'User-agent': str_user_agent}
    resp = requests.get(url, headers=header)

    # not working properly
    if resp.status_code == 200:
        return resp.content.decode()
    else:
        return False


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


def sort_top_words_general(words):
    return sorted(words.items(), key=lambda item: item[1], reverse=True)


def spider_specific_url(url, length, how_much_words):
    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, length)

    for i in range(how_much_words):
        # print(f'{top_words[i][0]}') prints out the specic word
        top_words_general(top_words[i][0], top_words[i][1])


def top_words_general(word, amount):
    global words_from_different_urls

    if word not in words_from_different_urls:
        words_from_different_urls[word] = amount
    else:
        current_count = words_from_different_urls.get(word)
        words_from_different_urls[word] += amount


def read_wfuzz_file(src):
    url_list = []

    with open(src) as file:
        json_data = json.load(file)

    for i in json_data:
        if i['url'] not in url_list:
            url_list.append(i['url'])

    return url_list


def print_result(sorted_words, size):
    counter = 0
    print("{:<6} {:<20} {:<10}".format('Pos', 'Word', 'Quantity'))
    for word in sorted_words:
        counter += 1
        print("{:<6} {:<20} {:<10}".format(counter, word[0], word[1]))

        if counter == int(size):
            break


def output_to_file(path, sorted_words):
    output = ""
    for word in sorted_words:
        output += f'{word[0]}\n'
    with open(path, 'w') as file:
        file.write(output)


@click.command()
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--source', '-src', prompt='Specify the JSON file from wfuzz', help='Specify the JSON file from wfuzz')
@click.option('--useragent', '-ua', help='Specify the User-Agent to send. Default is "python-requests/2.28.1"')
@click.option('--output', '-o', help='Write the output to the file.')
@click.option('--size', '-s', prompt='How many words should be generated?', help='The most popular words will be written into the wordlist. Here you have to define how many words you want to have in the wordlist.')
def main(length, source, size, output, useragent):
    """WLS 1.2 (https://github.com/pa4ul/WLS)"""
    global user_agent

    user_agent = useragent

    url_list = read_wfuzz_file(source)
    for url in url_list:
        try:
            get = requests.get(url)
            if get.status_code == 200:
                spider_specific_url(url, length, int(size))
        except:
            print("NOT WORKING CORRECTLY")

    sorted_words = sort_top_words_general(words_from_different_urls)
    print_result(sorted_words, size)
    if output is not None:
        output_to_file(output, sorted_words)


if __name__ == '__main__':
    main()
