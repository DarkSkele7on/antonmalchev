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
        params = {"key": self.api_key, "q": keywords, "part": "snippet", "type": "video", "order": sort_by, "maxResults": max_results}

        # Filter the results by date and relevance
        if sort_by == "date":
            params["publishedAfter"] = published_after
        elif sort_by == "relevance":
            params["relevanceLanguage"] = "en"

        # Handle pagination
        next_page_token = ""
        suggestions = []
        while True:
            # Add the next page token to the query parameters
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make the API request
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"An error occurred while making the API request: {e}")
                break

            # Parse the JSON response
            data = response.json()
            items = data.get("items", [])
            suggestions.extend(items)

            # Check if there are more pages of results
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
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
        print(video["title"] + " - " + video["url"])

# Create an instance of the YouTubeClient class
client = YouTubeClient("AIzaSyD002GWfSYFQP7h0bVvITqVvFoYvXkj09E")

# Search for videos based on the keywords
keywords = ["self improvement", "fitness", "money making"]
client.search(keywords)
client.suggest()