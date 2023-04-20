import queue
import csv
import cloudscraper
from bs4 import BeautifulSoup
# def load_proxy():
#     q = queue.Queue()
#     with open("../proxy_list.txt", "r") as f:
#         proxies = f.read().split("\n")
#         for p in proxies:
#             q.put(p)
#     return q

# def load_proxy():
#     q = queue.Queue()
#     with open("../Free_Proxy_List.csv", "r") as f:
#         proxies = csv.DictReader(f, delimiter=',', quotechar='"')
#         # proxies = f.read().split("\n")
#         for p in proxies:
#             q.put(p["ip"])
#     return q


def load_proxy():
    scraper = cloudscraper.create_scraper()
    page = scraper.get("https://free-proxy-list.net/")

    print(page.status_code)
    soup_page = BeautifulSoup(page.text, 'lxml')

    table_ip = soup_page.find('table', class_="table table-striped table-bordered")

    all_ip = table_ip.find_all('tr')

    q = queue.Queue()
    for p in all_ip[1:]:
        ip_and_ports = p.findAll('td')
        q.put(f'{ip_and_ports[0].text}:{ip_and_ports[1].text}')
    return q

if __name__ == "__main__":
    a = load_proxy()
    print('hola')