import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import string
import nltk
from nltk.stem.porter import PorterStemmer

#zaczynamy od nowa
#1) złapać wszystkie url
#2) użyć kodu z crawl_tokenize_makeinvertedindex to make index out of those  - robienie indeksu działa, tylko problemem jest czytanie URLS
#3) write it all to the csv file
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.index = {}

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

        #self.make_inverted_index()
        return self.visited_urls


#if __name__ == '__main__':
#    Crawler(urls=['http://example.python-scraping.com/']).run()