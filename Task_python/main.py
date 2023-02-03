import requests
from bs4 import BeautifulSoup

url = "https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

try:
    name = soup.find("h1", {"class": "product-name"}).text.strip()
    price = soup.find("span", {"class": "S5XGZ text-title-xl"}).text.strip()
    price = float(price.split(" ")[-1].replace(",", "."))
    color = soup.find("span", {"itemprop": "color", "class": "colors-info-name"}).text.strip()
    sizes = []
    for size in soup.find_all("span", {"class": "text-title-m gk2V5"}):
        sizes.append(size.text.strip())
    product = {
        "name": name,
        "price": price,
        "color": color,
        "sizes": sizes,
    }
    print(product)
except Exception as e:
    print(f"Error while scraping the data: {e}")
