import random
import requests
import webbrowser

class YouTubeClient:
    videos = []
    def __init__(self, api_key, videos = []):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        self.videos = videos or []

    def search(self, keywords, sort_by="relevance", published_after="2020",max_results=10):
        # Use the YouTube API to search for videos based on the keywords
        parameters = {"key": self.api_key, "q": keywords, "part": "snippet", "type": "video", "order": sort_by, "maxResults": max_results}

        # Filter the results by date and relevance
        if sort_by == "date":
            parameters["publishedAfter"] = published_after
        elif sort_by == "relevance":
            parameters["relevanceLanguage"] = "en"

        # Handle pagination
        next_page_token = ""
        suggestions = []
        while True:
            # Add the next page token to the query parameters
            if next_page_token:
                parameters["pageToken"] = next_page_token

            # Make the API request
            try:
                with requests.get(self.base_url, params=parameters) as response:
                    response.raise_for_status()

                    # Parse the JSON response
                    data = response.json()
                    items = data.get("items", [])
                    suggestions.extend(items)

                    # Check if there are more pages of results
                    next_page_token = data.get("nextPageToken")
                    if not next_page_token:
                        break
            except requests.RequestException as e:
                print(f"An error occurred while making the API request: {e}")
                break

        # Extract the video titles and URLs from the response
        for video in suggestions:
            title = video["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            self.videos.append({"title": title, "url": url})

        # Return the list of videos
        return self.videos

    def suggest(self):
        if not self.videos:
            return
        # Select a random video from the search results
        video = random.choice(self.videos)

        # Open the video in the web browser
        webbrowser.open_new(video["url"])

        # Print the video URL and title
        return video
    def download(self, file_name):
        # Use the `suggest()` method to select a random video from the search results
        video = self.suggest()
        if video is None:
            return

        # Get the video URL from the selected video
        url = video["url"]

        # Make a GET request to the specified URL
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"An error occurred while downloading the file: {e}")
            return

        # Open the file for writing in binary mode
        with open(file_name, "wb") as f:
            # Write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"File successfully downloaded: {file_name}")

# Create an instance of the YouTubeClient class
client = YouTubeClient("AIzaSyD002GWfSYFQP7h0bVvITqVvFoYvXkj09E")

# Search for videos based on the keywords
keywords = ["self improvement", "fitness", "money making", "hustle","money","investing","get rich","millionaire"]

client.search(keywords)
client.download("suggested_videos.txt")
client.suggest()