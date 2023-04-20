from bs4 import BeautifulSoup
import requests


rawPage = requests.get('https://www.pccomponentes.com/tarjetas-graficas').text


page = BeautifulSoup(rawPage, 'lxml')

print(page)


