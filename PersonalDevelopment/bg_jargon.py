import requests
from bs4 import BeautifulSoup

def get_word_of_the_day():
    # Make a request to the website
    response = requests.get("https://www.bgjargon.com/")

    # Parse the HTML of the website
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element containing the word of the day
    word_of_the_day_element = soup.find(class_='wotd-word')
    if word_of_the_day_element:
        # Return the word of the day if the element was found
        return word_of_the_day_element.text
    else:
        # Return an error message if the element was not found
        return "Error: Could not find word of the day"

word_of_the_day = get_word_of_the_day()
print(f"The word of the day is: {word_of_the_day}")

