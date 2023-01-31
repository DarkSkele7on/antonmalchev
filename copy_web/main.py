from selenium import webdriver

browser = webdriver.Firefox()
browser.get(url)
html = browser.page_source

with open("webpage.html", "w") as f:
    f.write(html)
browser.quit()
