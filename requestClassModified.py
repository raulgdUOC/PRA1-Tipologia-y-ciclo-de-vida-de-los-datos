"""
This module provide the class requestModified which it will help us to the labor of
changing the IP form a proxi which doesn't work to others.
"""

import cloudscraper
from bs4 import BeautifulSoup
import bs4
import queue
import threading
import requests


class RequestModified:
    """
    This class is an improved version of cloudscraper with the advantage of perform request with a queue of
    proxies. This queue will be updated everytime that the code reach the end of the queue.
    """
    def __init__(self):
        self.scrapper = cloudscraper.create_scraper()
        self.load_proxy()  # Loading for first time the queue of proxies
        self.lock = threading.Lock()

    def load_proxy(self) -> None:
        """
        Load the queue of proxies.
        """

        # Loading the page and getting the soup
        page: requests.models.Response = self.scrapper.get("https://free-proxy-list.net/")
        soup_page: BeautifulSoup = BeautifulSoup(page.text, 'lxml')

        # Getting the tag of the table with the IPs
        table_ip: bs4.element.Tag = soup_page.find('table', class_="table table-striped table-bordered")
        all_ip: bs4.element.ResultSet = table_ip.find_all('tr')
        queue_IP:  queue.Queue = queue.Queue()

        # Loop to get the IP and the port
        for ip in all_ip[1:]:
            ip_and_ports = ip.findAll('td')
            queue_IP.put(f'{ip_and_ports[0].text}:{ip_and_ports[1].text}')

        # Saving the queue in a property
        self.proxys: queue.Queue = queue_IP

    def get(self, url_page: str, header: dict) -> str:
        """
        Method to get the HTML code of the page, looping over the queue of proxies until finding a proxi which works.

        Args:
            url_page (str): URL of the page with the HTML code desire.
            header (dict): Dictionary with the headers for the request.
        Return
        str: HTML code of the URL.
        """
        while True:
            self.lock.acquire()
            proxy: str = self.proxys.get()  # Taking an IP from the queue
            self.lock.release()

            # If the queue is empty, it will be load again
            if self.proxys.empty():
                self.load_proxy()

            # Trying to do a request. If it doesn't success, it will take the next IPs.
            try:
                res = self.scrapper.get(url_page,
                                        proxies={"http": proxy,
                                                 "https": proxy},
                                        headers=header,
                                        timeout=10)

            except Exception as e:
                # print(e)
                continue

            # If the result of the request is 200, it returns the code as string.
            if res.status_code == 200:
                self.lock.acquire()
                self.proxys.put(proxy)
                self.lock.release()
                return res.text




