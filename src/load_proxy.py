"""
This module provides tools to help in the labor of do webscraping. These tools are load_proxy and progress_bar. The
first return a queue with IP of proxy servers and the other print the progres of the program.
"""
import queue
import cloudscraper
from bs4 import BeautifulSoup


def load_proxy():
    """
    Return a queue with IPs from proxies caught from a webpage.
    Return:
        queue.Queue: Queue of proxies.
    """
    scraper = cloudscraper.create_scraper()
    page = scraper.get("https://free-proxy-list.net/")  # Request to the page with proxies

    soup_page = BeautifulSoup(page.text, 'lxml')

    table_ip = soup_page.find('table', class_="table table-striped table-bordered")

    all_ip = table_ip.find_all('tr')

    q = queue.Queue()
    for p in all_ip[1:]:
        ip_and_ports = p.findAll('td')
        q.put(f'{ip_and_ports[0].text}:{ip_and_ports[1].text}')
    return q

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"{progress}|{bar}| {percent:.2f}%", end="\r")


if __name__ == "__main__":
    a = load_proxy()
    print('hola')