import requests
from bs4 import BeautifulSoup

url = 'https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

product_name = soup.find('h1', {'itemprop': 'name', 'class': 'product-name'}).text
price = soup.find('span', {'data-testid': 'currentPrice'}).find('span', {'class': 'S5XGZ text-title-xl'}).text
color = soup.find('span', {'itemprop': 'color', 'class': 'colors-info-name'}).text

sizes = []
for size in soup.find_all('span', class_='gk2V5'):
    sizes.append(size)

print('Name:', product_name)
print('Price:', price)
print('Color:', color)
print('Sizes:', sizes)
