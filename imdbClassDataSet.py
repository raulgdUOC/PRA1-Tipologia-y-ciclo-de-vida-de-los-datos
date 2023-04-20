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

import csv
class imdbDataSet:
    def __init__(self, genere, type_):
        self.lock = threading.Lock()
        self.proxys = load_proxy()
        self.scrapper = cloudscraper.create_scraper()
        self.genere = genere
        self.title_type = type_
        self.templateURL = self.generateURL()
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


    def get_response(self, URL: str):
        while True:
            self.lock.acquire()
            proxy = self.proxys.get()
            self.lock.release()
            if self.proxys.empty():
                print("LOADING")
                self.proxys = load_proxy()

            try:
                # sleep(randint(1, 2))
                res = self.scrapper.get(URL,
                                        proxies={"http": proxy,
                                                 "https": proxy},
                                        headers=self.header,
                                        timeout=10)

            except Exception as e:
                # print(e)
                continue
            if res.status_code == 200:
                # print(res.status_code)
                self.lock.acquire()
                self.proxys.put(proxy)
                self.lock.release()
                return res
            else:
                print(res.status_code)




    def generateURL(self) -> str:
        return f'https://www.imdb.com/search/title/?title_type={self.title_type}&genres={self.genere}' \
               '&start={}&explore=title_type,genres&ref_=adv_nxt'

    def nextURL(self, num_of_web_page: int) -> str:
        return self.templateURL.format(num_of_web_page)

    def getHTML(self, URL: str) -> bs4.BeautifulSoup:
        raw_page = self.get_response(URL)
        # raw_page: str = self.scrapper.get(URL, headers=self.header).text
        return BeautifulSoup(raw_page.text, 'lxml')
    def getNameContent(self, tag: bs4.BeautifulSoup) -> str:
        try:
            return tag.find('div', class_='lister-item-content').h3.a.text
        except:
            return "NA"

    def getReleseYear(self, tag: bs4.BeautifulSoup) -> str:
        try:
            tag_h3:  bs4.BeautifulSoup = tag.find('div', class_='lister-item-content').h3
            return tag_h3.find('span', class_='lister-item-year text-muted unbold').text
        except:
            return "NA"

    def getTimeContent(self, tag: bs4.BeautifulSoup) -> str:
        try:
            tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
            tag_p: bs4.BeautifulSoup = tag_div.find('p', class_='text-muted')
            return tag_p.find('span', class_='runtime').text
        except:
            return "NA"

    def getCertificate(self, tag: bs4.BeautifulSoup) -> str:
        try:
            return tag.find('span', class_='certificate').text
        except:
            return "NA"

    def getAllGeneres(self, tag: bs4.BeautifulSoup) -> str:
        try:
            tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
            tag_p: bs4.BeautifulSoup = tag_div.find('p', class_='text-muted')
            return tag_p.find('span', class_='genre').text
        except:
            return "NA"

    def getRatingImdb(self, tag: bs4.BeautifulSoup) -> str:
        try:
            tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
            tag_div2: bs4.BeautifulSoup = tag_div.find('div', class_='ratings-bar')
            return tag_div2.find('div', class_='inline-block ratings-imdb-rating').strong.text
        except:
            return "NA"

    def getRatingMetacritic(self, tag: bs4.BeautifulSoup) -> str:
        try:
            tag_div: bs4.BeautifulSoup = tag.find('div', class_='lister-item-content')
            tag_div2: bs4.BeautifulSoup = tag_div.find('div', class_='ratings-bar')
            return tag_div2.find('div', class_='inline-block ratings-metascore').span.text
        except:
            return "NA"

    def getPageContent(self, tag: bs4.BeautifulSoup):
        URI_page = tag.find("div", class_="lister-item-content").h3.a.get("href")
        URL = f"https://www.imdb.com{URI_page}"

        film_page_content = self.get_response(URL)
        # film_page_content = self.scrapper.get(f"https://www.imdb.com{URI_page}").text

        soup_film_page = BeautifulSoup(film_page_content.text, "lxml")
        return soup_film_page

    def getCasting(self, soup_page_film: bs4.BeautifulSoup):
        casting = []
        soup_casting = soup_page_film.findAll("a", class_="sc-bfec09a1-1 fUguci")
        for cast in soup_casting:
            casting.append(cast.text)

        return casting

    def getDirector(self, soup_page_film: bs4.BeautifulSoup):
        Director = []
        soup_director = soup_page_film.findAll("li", class_="ipc-metadata-list__item")[0]

        soup_director = soup_director.findAll("a", class_="ipc-metadata-list-item__list-content-item " \
                                                           "ipc-metadata-list-item__list-content-item--link")

        for director in soup_director:
            Director.append(director.text)

        return Director

    def getWriters(self, soup_page_film: bs4.BeautifulSoup):
        Writers = []
        soup_writers = soup_page_film.findAll("li", class_="ipc-metadata-list__item " \
                                                          "ipc-metadata-list-item--link")[1]

        soup_writers = soup_writers.findAll("a", class_="ipc-metadata-list-item__list-content-item " \
                                                          "ipc-metadata-list-item__list-content-item--link")

        for director in soup_writers:
            Writers.append(director.text)

        return Writers



    def getTagFilms(self, raw_page: bs4.BeautifulSoup) -> bs4.element.ResultSet:

        return raw_page.findAll('div', class_='lister-item mode-advanced')


    def pipeFunctions(self, tag_film):
        soup_page_film = self.getPageContent(tag_film)
        self.dataset["NameContent"].append(self.getNameContent(tag_film))
        self.dataset["ReleseYear"].append(self.getReleseYear(tag_film))
        self.dataset["Certificate"].append(self.getCertificate(tag_film))
        self.dataset["TimeContent"].append(self.getTimeContent(tag_film))
        self.dataset["AllGeneres"].append(self.getAllGeneres(tag_film))
        self.dataset["RatingImdb"].append(self.getRatingImdb(tag_film))
        self.dataset["RatingMetacritic"].append(self.getRatingMetacritic(tag_film))
        self.dataset["Casting"].append(self.getCasting(soup_page_film))
        self.dataset["Directors"].append(self.getDirector(soup_page_film))
        self.dataset["Writers"].append(self.getWriters(soup_page_film))

        self.films_scraped += 1
        print(self.films_scraped)
    def scrapPage(self, numPage):
        URL_to_scrap: str = self.nextURL(numPage)

        raw_page: bs4.BeautifulSoup = self.getHTML(URL_to_scrap)

        tags_films: bs4.element.ResultSet = self.getTagFilms(raw_page)

        # for tag_film in tags_films:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.pipeFunctions, tags_films)
                # self.pipeFunctions(tag_film)

    def saveDataset(self):
        df = pd.DataFrame.from_dict(self.dataset)
        df.to_csv("dataset.csv", index=False)

    def __call__(self, num_of_page=1):
        for actual_num_page in range(1, 50*num_of_page + 1, 50):
        # with concurrent.futures.ThreadPoolExecutor() as executor:
            self.scrapPage(actual_num_page)
            # executor.map(self.scrapPage, list(range(1, 50*num_of_page + 1, 50)))

            # print(self.getPageContent(tag_film))





if __name__ == '__main__':

    prueba = imdbDataSet(type_='movie', genere='comedy')
    prueba(199)
    prueba.saveDataset()
    print(prueba.dataset["Casting"])












