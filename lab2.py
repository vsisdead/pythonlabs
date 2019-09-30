import collections
import re

from bs4 import BeautifulSoup
from requests import request
import matplotlib.pyplot as plt
import pandas as pd
import operator
import sys
from itertools import islice

def get_all_links(link_from):
    req = request('GET', link_from)
    soup = BeautifulSoup(req.text, 'html.parser')
    href = []
    links = soup.find_all('a', href=True)
    print('Got {} links.'.format(len(links)))
    for a in links:
        href.append(a['href'])
    return list(filter(lambda a: a != '#', href))


def get_text(link_from):
    req = request('GET', link_from)
    soup = BeautifulSoup(req.text, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text().replace(',', '').replace(' ', '').replace('\n', '').lower()

    result = ''

    for char in text:
        if re.match(r'^[а-яА-я]$', char):
            result += char
    return result


def get_all_words(link_from):
    req = request('GET', link_from)
    soup = BeautifulSoup(req.text, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    words = text.replace(',', '').split()

    for i, word in enumerate(words):
        if re.match(r'^\d+$', word):
            words.pop(i)

    return words


def count_chars(text):
    c = collections.Counter(text)
    return c


def count_words(words):
    c = collections.Counter(words)
    return dict(c)


def count_symbols(words):
    counter = []

    for word in words:
        counter.append(len(word))

    c = collections.Counter(counter)
    result = {}
    for key in sorted(c.keys()):
        result[key] = c[key]

    return result

def take(n, iterable):
    return dict(islice(iterable, n))

def draw_plot(values, lbx='xplot', lby='yplot'):
    plt.bar(range(len(values)), list(values.values()), align='center')
    plt.xlabel(lbx)
    plt.ylabel(lby)
    plt.xticks(range(len(values)), list(values.keys()))
    plt.show()

try:
    link = sys.argv[1]
except:
    link = 'http://yandex.by'

statistics = {}
counter = 0

links = get_all_links(link)

for a_link in get_all_links(link):
    counter += 1
    try:
        statistics[a_link] = {
            'urls': len(get_all_links(a_link)),
            'words': list(count_words(get_all_words(a_link)).keys()),
            'chars': list(count_symbols(get_all_words(a_link)).keys())
        }
    except:
        print('invalid link')
    if counter > 4:
        break

df = pd.DataFrame(data=statistics)
print(df)
#
sorted_words = {}
for elem in sorted(count_words(get_all_words(link)).items(), key=operator.itemgetter(1), reverse=True) :
    sorted_words[elem[0]] = elem[1]
draw_plot(take(10, sorted_words.items()), 'Words', 'Occurrences')
draw_plot(count_symbols(get_all_words(link)), 'Word length', 'Amount words')
draw_plot(count_chars(get_text(link)), 'Letters', 'Amount')
#
# for i in range(1, 3):
#     inner_links = get_all_links(links[i])
#     for j in range(1, 3):
#         draw_plot(count_chars(get_text(inner_links[j])), 'Letters', 'Amount')
#         k_links = get_all_links(inner_links[j])
#         for k in range(1, 3):
#              draw_plot(count_chars(get_text(k_links[k])), 'Letters', 'Amount')



