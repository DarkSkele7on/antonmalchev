from selenium import webdriver
import time

# Initialize a webdriver instance
driver = webdriver.Chrome()

# Navigate to the product page
driver.get("https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99")

# Wait for the page to load
time.sleep(10)
# Check if the cookie consent pop-up is present
try:
    language_button = driver.find_element_by_xpath("//a[@data-lang='en']")
    language_button.click()
    cookie_popup = driver.find_element_by_id("CybotCookiebotDialogBodyButtonAccept")
    cookie_popup.click()
    
except:
    pass

parent_element = driver.find_element_by_xpath("//*[@id='productDesktop']/main/div/div[2]/div[2]/div")
name = parent_element.find_element_by_xpath("h1").text

# Retrieve the price using xpath
price = parent_element.find_element_by_xpath(".//span[@class='S5XGZ text-title-xl']").text

# Retrieve the color using xpath
color = parent_element.find_element_by_xpath(".//span[@itemprop='color']").text

# Retrieve the size using xpath
size = parent_element.find_element_by_xpath(".//span[@id='size-19']").text

# Store the data in a dictionary
data = {
    "name": name,
    "price": price,
    "color": color,
    "size": size
}

# Output the data to a json file
import json
with open("product_info.json", "w") as outfile:
    json.dump(data, outfile)

# Close the webdriver instance
driver.close()
