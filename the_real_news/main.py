import requests
from bs4 import BeautifulSoup

class NewsSynthesizer:
  def __init__(self, topic):
    self.topic = topic
    self.news_sources = ["http://www.bbc.com/news", "http://www.cnn.com/world", "http://www.reuters.com"]
    self.extracted_information = []

  def extract_information(self):
    # Loop through each news source
    for source in self.news_sources:
      # Use the requests library to download the HTML of the news source
      html = requests.get(source).text

      # Use BeautifulSoup to parse the HTML and extract the relevant information
      soup = BeautifulSoup(html, "html.parser")
      articles = soup.find_all("article")
      for article in articles:
        # Use the article's headline and summary classes to find the relevant elements
        # Note: the class names might be different on each news source, so you may have to adjust them
        # to match the correct elements on each website.
        title = article.find(class_="story-body__h1").text
        summary = article.find(class_="story-body__inner").text
        self.extracted_information.append((title, summary))

  def synthesize_text(self):
    # Synthesize the extracted information into a single text in English
    synthesized_text = ""
    for info in self.extracted_information:
      synthesized_text += info[0] + ": " + info[1] + "\n"
    # Return the synthesized text
    return synthesized_text

  def write_to_file(self, file_name):
    with open(file_name, "w") as file:
      file.write(self.synthesize_text())


# Create a NewsSynthesizer object for the topic "climate change"
synthesizer = NewsSynthesizer("climate change")


# Extract the information from the news sources
synthesizer.extract_information()

# Synthesize the information into a single text
synthesized_text = synthesizer.synthesize_text()
print(synthesized_text)

with open("climate_change_news.txt", "w") as file:
      file.write(synthesized_text)
# Write the synthesized text to a file called "climate_change_news.txt"
#synthesizer.write_to_file("climate_change_news.txt")
