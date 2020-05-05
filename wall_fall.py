#!/usr/bin/env python3

import argparse
import re
import requests
from bs4 import BeautifulSoup as bs

# takes a url to a paywalled sz article and print the text behind the wall
def sz_extractor(url):
    html_article = requests.get(url)
    bs_article = bs(html_article.text, 'html.parser')
    # this could be easier, but the sz journalists format text like my granny..
    for p in bs_article.find(class_ = 'article-content paywall').find_all('p'):
        print(p.getText(strip=True))


# takes a url to a paywalled dnn article and print the text behind the wall
def dnn_extractor(url):
    html_article = requests.get(url)
    bs_article = bs(html_article.text, 'html.parser')
    headline_pattern = re.compile('"(headline)":"(.*?)"')
    article_pattern = re.compile('"(articleBody)":"(.*?)"')
    for s in bs_article.find_all('script', type="application/ld+json"):
        if re.findall(article_pattern, s.text):
            js = s
            break

    _, headline = re.findall(headline_pattern, js.text)[0]
    _, article = re.findall(article_pattern, js.text)[0]
    print(headline)
    print(article)

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        metavar = 'URL',
        help = 'url of a sz or dnn article behind an paywall',
        type = str)

    args = parser.parse_args()

    dnn_pat = re.compile("(dnn\.de)")
    sz_pat = re.compile("(saechsische\.de)")
    if re.findall(dnn_pat, args.url):
        dnn_extractor(args.url)
    elif re.findall(sz_pat, args.url):
        sz_extractor(args.url)
    else:
        print('Neither a sz, or a dnn link')
