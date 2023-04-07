import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
from urllib.parse import urlsplit

class WebScraper:
    def __init__(self, pages):
        self.pages = pages
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        self.proxies = {
              'http': 'http://IP:PORT',
              'https': 'http://IP:PORT',
        }
    
    def get_data(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies)
        except:
            response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("title").get_text()
        content = soup.get_text()
        return title, content

    def get_data_from_multiple_pages(self):
        data = []
        for page in self.pages:
            data.append(self.get_data(page))
        return data

    def write_to_csv(self, data):
        for url, (title, content) in zip(self.pages, data):
            parsed_url = urlsplit(url)
            file_name = parsed_url.netloc + ".csv"
            df = pd.DataFrame({'Title': [title], 'Content': [content]})
            if not os.path.exists(file_name):
                df.to_csv(file_name, index=False)
            else:
                df.to_csv(file_name, mode='a', header=False, index=False)

if __name__ == "__main__":
    pages = sys.argv[1:]
    scraper = WebScraper(pages)
    data = scraper.get_data_from_multiple_pages()
    scraper.write_to_csv(data)
