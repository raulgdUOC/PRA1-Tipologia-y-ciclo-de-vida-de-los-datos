import bs4
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
import threading
import concurrent.futures
from load_proxy import *
from time import sleep
from random import randint
from requestClassModified import RequestModified
import csv


class ImdbDataSet:
    def __init__(self, genre, type_):
        self.lock = threading.Lock()
        self.proxys = load_proxy()
        self.scrapper = cloudscraper.create_scraper()
        self.genre = genre
        self.title_type = type_
        self.templateURL = self.__generate_url()
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


    def __get_response(self, url_page: str):
        """
        Method to get the HTML code of the page, looping over the queue of proxies until finding a proxi which works.

        Args:
            url_page (str): URL of the page with the HTML code desire.

        Return
        str: HTML code of the URL.
        """

        # If the response code is 50 times different from 200
        not_successful_code = 0
        while not_successful_code <= 50:
            print(f'The size of the queue is:{self.proxys.qsize()}')
            self.lock.acquire()
            proxy = self.proxys.get()  # Taking an IP from the queue

            # If the queue is empty, it will be load again
            if self.proxys.empty():
                print("LOADING")
                self.proxys = load_proxy()
            self.lock.release()
            # Use of try-exception clausures dude to the exceptions that some proxies can through
            try:
                res = self.scrapper.get(url_page,
                                        proxies={"http": proxy,
                                                 "https": proxy},
                                        headers=self.header,
                                        timeout=10)

            except Exception as e:
                print(e)
                continue
            if res.status_code == 200:
                # self.lock.acquire()
                self.proxys.put(proxy)
                # self.lock.release()
                return res

            else:
                not_successful_code += 1
        raise Exception("The server has refused a lot of time your request, please, try more later.")

    def __generate_url(self) -> str:
        """
        Return a template of the url with the content and the genre desire. The number of page is prepared to be
        introduced.
        Return:
            str: The template url.
        """
        return f'https://www.imdb.com/search/title/?title_type={self.title_type}&genres={self.genre}' \
               '&start={}&explore=title_type,genres&ref_=adv_nxt'

    def __next_url(self, num_of_web_page: int) -> str:
        """
        Return the url of the page with the number desire.
        Args:
            num_of_web_page (int): Number of the page.
        Return:
            str: The url of the page.
        """
        return self.templateURL.format(num_of_web_page)

    def __get_html(self, page_url: str) -> bs4.BeautifulSoup:
        """
        Return the HTML code of the page in format  BeautifulSoup.
        Args:
            page_url (str): The url of the page.
        Return:
            bs4.BeautifulSoup: The code of the page in format BeautifulSoup.
        """
        raw_page = self.__get_response(page_url)
        return BeautifulSoup(raw_page.text, 'lxml')

    def __get_name_content(self, tag_content: bs4.BeautifulSoup) -> str:
        """
        Return the name of the content.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            str: The name of the content.
        """
        try:
            return tag_content.find('div', class_='lister-item-content').h3.a.text
        except AttributeError:
            return "NA"

    def __get_relese_year(self, tag: bs4.BeautifulSoup) -> str:
        try:
            tag_h3:  bs4.BeautifulSoup = tag.find('div', class_='lister-item-content').h3
            return tag_h3.find('span', class_='lister-item-year text-muted unbold').text
        except AttributeError:
            return "NA"

    def __get_time_content(self, tag_content: bs4.BeautifulSoup) -> str:
        """
        Return the duration of the content.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            str: The duration of the content.
        """
        try:
            tag_div: bs4.BeautifulSoup = tag_content.find('div', class_='lister-item-content')
            tag_p: bs4.BeautifulSoup = tag_div.find('p', class_='text-muted')
            return tag_p.find('span', class_='runtime').text
        except AttributeError:
            return "NA"

    def __get_certificate(self, tag_content: bs4.BeautifulSoup) -> str:
        """
        Return for which audience it is directed.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            str: The certificate for the public.
        """
        try:
            return tag_content.find('span', class_='certificate').text
        except AttributeError:
            return "NA"

    def __get_all_genres(self, tag_content: bs4.BeautifulSoup) -> str:
        """
        Return the genres of the content if they are available.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            str: The genres of the content.
        """
        try:
            tag_div: bs4.BeautifulSoup = tag_content.find('div', class_='lister-item-content')
            tag_p: bs4.BeautifulSoup = tag_div.find('p', class_='text-muted')
            return tag_p.find('span', class_='genre')
        except AttributeError:
            return "NA"

    def __get_rating_imdb(self, tag_content: bs4.BeautifulSoup) -> str:
        """
        Return the rating IMDb of the content if it is available.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            str: The rating of IMDb.
        """
        try:
            tag_div: bs4.BeautifulSoup = tag_content.find('div', class_='lister-item-content')
            tag_div2: bs4.BeautifulSoup = tag_div.find('div', class_='ratings-bar')
            return tag_div2.find('div', class_='inline-block ratings-imdb-rating').strong.text
        except AttributeError:
            return "NA"

    def __get_rating_metacritic(self, tag_content: bs4.BeautifulSoup) -> str:
        """
        Return the rating metacritic of the content if it is available.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            str: The rating of metacritic.
        """
        try:
            tag_div: bs4.BeautifulSoup = tag_content.find('div', class_='lister-item-content')
            tag_div2: bs4.BeautifulSoup = tag_div.find('div', class_='ratings-bar')
            return tag_div2.find('div', class_='inline-block ratings-metascore').span.text
        except AttributeError:
            return "NA"

    def __get_casting(self, soup_page_film: bs4.BeautifulSoup):
        """
        Return the information about the casting of the content selected.
        Args:
            soup_page_film (bs4.BeautifulSoup): The page of the content in format BeautifulSoup.
        Return:
            list: List with the casting of the content.
        """
        casting = []
        soup_casting = soup_page_film.findAll("a", class_="sc-bfec09a1-1 fUguci")
        for cast in soup_casting:
            casting.append(cast.text)

        return casting

    def __get_director(self, soup_page_film: bs4.BeautifulSoup):
        """
        Return the information about the directors of the content selected.
        Args:
            soup_page_film (bs4.BeautifulSoup): The page of the content in format BeautifulSoup.
        Return:
            list: List of the directors of the content.
        """
        directors = []
        soup_director = soup_page_film.findAll("li", class_="ipc-metadata-list__item")[0]

        soup_director = soup_director.findAll("a", class_="ipc-metadata-list-item__list-content-item " \
                                                           "ipc-metadata-list-item__list-content-item--link")

        for directors in soup_director:
            directors.append(directors.text)

        return directors

    def __get_writers(self, soup_page_film: bs4.BeautifulSoup):
        """
        Return the information about the writers of the content selected.
        Args:
            soup_page_film (bs4.BeautifulSoup): The page of the content in format BeautifulSoup.
        Return:
            list: List of the writers of the content.
        """
        writers = []
        soup_writers = soup_page_film.findAll("li", class_="ipc-metadata-list__item " \
                                                          "ipc-metadata-list-item--link")[1]

        soup_writers = soup_writers.findAll("a", class_="ipc-metadata-list-item__list-content-item " \
                                                          "ipc-metadata-list-item__list-content-item--link")

        for director in soup_writers:
            writers.append(director.text)

        return writers

    def __get_tags(self, raw_page: bs4.BeautifulSoup) -> bs4.element.ResultSet:
        """
        Return a list with the 50 tags with information of each content selected (films, TV series, etc).

        Args:
            raw_page (bs4.BeautifulSoup): The HTML code of the principal page without modifications.
        Return:
            list: List with the 50 tags with information about the content selected.
        """

        return raw_page.findAll('div', class_='lister-item mode-advanced')

    def __get_film_page(self, tag_content: bs4.BeautifulSoup):
        """
        Return the page of the content selected in BeautifulSoup format from the tag obtained from the principal page.
        Args:
            tag_content (bs4.BeautifulSoup): Tag with information about the content selected.
        Return:
            bs4.BeautifulSoup: The page of the content selected from the tag.
        """
        uri_page = tag_content.find("div", class_="lister-item-content").h3.a.get("href")
        url_page = f"https://www.imdb.com{uri_page}"

        film_page_content = self.__get_response(url_page)

        soup_film_page = BeautifulSoup(film_page_content.text, "lxml")
        # soup_film_page = self.__get_response(url_page)
        return soup_film_page

    def __pipe_functions(self, tag_content):
        """
        This method calls all the methods which catch the information to be saved in the dataset. At the
        same time, the information is saved in the dataset.

        Arg:
            tag_content (bs4.BeautifulSoup): Tag from the principal page, which contains short information
            of the content selected.

        Return:
            None
        """

        soup_page_film = self.__get_film_page(tag_content)  # Content from the page of the film
        # Append the data to the dataset
        self.dataset["NameContent"].append(self.__get_name_content(tag_content))
        self.dataset["ReleseYear"].append(self.__get_relese_year(tag_content))
        self.dataset["Certificate"].append(self.__get_certificate(tag_content))
        self.dataset["TimeContent"].append(self.__get_time_content(tag_content))
        self.dataset["Allgenres"].append(self.__get_all_genres(tag_content))
        self.dataset["RatingImdb"].append(self.__get_rating_imdb(tag_content))
        self.dataset["RatingMetacritic"].append(self.__get_rating_metacritic(tag_content))
        self.dataset["Casting"].append(self.__get_casting(soup_page_film))
        self.dataset["Directors"].append(self.__get_director(soup_page_film))
        self.dataset["Writers"].append(self.__get_writers(soup_page_film))

        self.films_scraped += 1
        print(self.films_scraped )
        # progress_bar(self.films_scraped, self.total_content )

    def __scrap_page(self, num_page):
        """
        Method for scrap the page which contains 50 cards of the content selected. For example, if the
        type_ variable is films, the 50 cards will have films.
        Args:
            num_page (int): Number of the page which is going to be scraped.
        Return:
            None.
        """
        url_to_scrap: str = self.__next_url(num_page)

        raw_page: bs4.BeautifulSoup = self.__get_html(url_to_scrap)

        tags_films: bs4.element.ResultSet = self.__get_tags(raw_page)

        # for tag_content in tags_films:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.__pipe_functions, tags_films)
        # threads = []
        # for tags in tags_films:
        #     t = threading.Thread(target=self.__pipe_functions, args=[tags])
        #     t.start()
        #     threads.append(t)
        # for thread in threads:
        #     thread.join()
    def save_dataset(self):
        """
        Method to save the variable dataset as csv with the name IMDb_data without index.
        Return:
            None
        """
        df_dataset = pd.DataFrame.from_dict(self.dataset)
        df_dataset.to_csv("IMDb_data.csv", index=False)

    def __call__(self, num_of_page=1):
        # self.total_content = num_of_page * 50
        # progress_bar(self.films_scraped, self.total_content)
        for actual_num_page in range(1, 50*num_of_page + 1, 50):
            self.__scrap_page(actual_num_page)







if __name__ == '__main__':

    prueba = ImdbDataSet(type_='movie', genre='comedy')
    prueba(200)
    prueba.save_dataset()









