import cloudscraper
import bs4
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
from validate_proxy import *
import threading
import concurrent.futures
from time import sleep
from random import randint
from requestClassModified import RequestModified
import csv
class imdbDataSet:
    def __init__(self, genere, type_):


        self.genere = genere
        self.title_type = type_
        self.scrapper = RequestModified()
        self.templateURL = self.generate_url()
        self.dataset = defaultdict(list)
        self.header = {
                        'Accept':
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive',
                        'DNT': '1',
                        'Host': 'www.imdb.com',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'None',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent':
                        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'
                        }
        self.films_scraped = 0

    def generate_url(self) -> str:
        return f'https://www.imdb.com/search/title/?title_type={self.title_type}&genres={self.genere}' \
               '&start={}&explore=title_type,genres&ref_=adv_nxt'

    def next_url(self, num_of_web_page: int) -> str:
        return self.templateURL.format(num_of_web_page)

    def get_html(self, url_html: str) -> BeautifulSoup:
        raw_page: str = self.scrapper.get(url_html, self.header)

        return BeautifulSoup(raw_page, 'lxml')

    def get_film_page(self, tag: BeautifulSoup) -> BeautifulSoup:
        URI_page = tag.find("div", class_="lister-item-content").h3.a.get("href")
        URL = f"https://www.imdb.com{URI_page}"

        soup_film_page = self.get_html(URL)
        return soup_film_page

    def pipeFunctions(self, tag_film):
        def get_name_content(tag: BeautifulSoup) -> str:
            try:
                return tag.find('div', class_='lister-item-content').h3.a.text
            except AttributeError:
                return "NA"

        def get_release_year(tag: BeautifulSoup) -> str:
            try:
                tag_h3: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content').h3
                return tag_h3.find('span', class_='lister-item-year text-muted unbold').text
            except AttributeError:
                return "NA"

        def get_time_content(tag: BeautifulSoup) -> str:
            try:
                tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
                tag_p: bs4.BeautifulSoup = tag_div.find('p', class_='text-muted')
                return tag_p.find('span', class_='runtime').text
            except AttributeError:
                return "NA"

        def get_certificate(tag: BeautifulSoup) -> str:
            try:
                return tag.find('span', class_='certificate').text
            except AttributeError:
                return "NA"

        def get_all_generes(tag: bs4.BeautifulSoup) -> str:
            try:
                tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
                tag_p: bs4.BeautifulSoup = tag_div.find('p', class_='text-muted')
                return tag_p.find('span', class_='genre').text
            except AttributeError:
                return "NA"

        def get_rating_imdb(tag: bs4.BeautifulSoup) -> str:
            try:
                tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
                tag_div2: bs4.BeautifulSoup = tag_div.find('div', class_='ratings-bar')
                return tag_div2.find('div', class_='inline-block ratings-imdb-rating').strong.text
            except AttributeError:
                return "NA"

        def get_rating_metacritic(tag: bs4.BeautifulSoup) -> str:
            try:
                tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
                tag_div2: bs4.BeautifulSoup = tag_div.find('div', class_='ratings-bar')
                return tag_div2.find('div', class_='inline-block ratings-metascore').span.text
            except AttributeError:
                return "NA"

        def get_casting(soup_film: BeautifulSoup):
            casting = []
            soup_casting = soup_film.findAll("a", class_="sc-bfec09a1-1 fUguci")
            for cast in soup_casting:
                casting.append(cast.text)

            return casting

        def get_director(soup_film: BeautifulSoup):
            director = []
            soup_director = soup_film.findAll("li", class_="ipc-metadata-list__item")[0]
            soup_director = soup_director.findAll("a", class_="ipc-metadata-list-item__list-content-item " \
                                                              "ipc-metadata-list-item__list-content-item--link")

            for director in soup_director:
                director.append(director.text)

            return director

        def get_writers(soup_film: bs4.BeautifulSoup):
            writers = []
            soup_writers = soup_film.findAll("li", class_="ipc-metadata-list__item " \
                                                               "ipc-metadata-list-item--link")[1]
            soup_writers = soup_writers.findAll("a", class_="ipc-metadata-list-item__list-content-item " \
                                                            "ipc-metadata-list-item__list-content-item--link")
            for director in soup_writers:
                writers.append(director.text)
            return writers

        soup_page_film = self.get_film_page(tag_film)
        self.dataset["NameContent"].append(get_name_content(tag_film))
        self.dataset["ReleseYear"].append(get_release_year(tag_film))
        self.dataset["Certificate"].append(get_certificate(tag_film))
        self.dataset["TimeContent"].append(get_time_content(tag_film))
        self.dataset["AllGeneres"].append(get_all_generes(tag_film))
        self.dataset["RatingImdb"].append(get_rating_imdb(tag_film))
        self.dataset["RatingMetacritic"].append(get_rating_metacritic(tag_film))
        self.dataset["Casting"].append(get_casting(soup_page_film))
        self.dataset["Directors"].append(get_director(soup_page_film))
        self.dataset["Writers"].append(get_writers(soup_page_film))

        self.films_scraped += 1
        print(self.films_scraped)
    def scrapPage(self, numPage):
        def get_tag_films(raw_page: bs4.BeautifulSoup) -> bs4.element.ResultSet:
            return raw_page.findAll('div', class_='lister-item mode-advanced')

        url_to_scrap: str = self.next_url(numPage)

        raw_page: BeautifulSoup = self.get_html(url_to_scrap)

        tags_films: bs4.element.ResultSet = get_tag_films(raw_page)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.pipeFunctions, tags_films)

    def save_dataset(self):
        df = pd.DataFrame.from_dict(self.dataset)
        df.to_csv("dataset.csv", index=False)

    def __call__(self, num_of_page=1):
        for actual_num_page in range(1, 50 * num_of_page + 1, 50):
            self.scrapPage(actual_num_page)






if __name__ == '__main__':
    prueba = imdbDataSet(type_='movie', genere='comedy')
    prueba(1)
    prueba.save_dataset()