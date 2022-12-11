from random import random
import requests
import random
import webbrowser

def suggest_videos(keywords, sort_by="relevance", published_after="", max_results=10):
    # Use the YouTube API to search for videos based on the keywords
    api_key = "AIzaSyDZvglFdfHLoaAlCJLBRNcqhYip2ytHDVk"
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {"key": api_key, "q": keywords, "part": "snippet", "type": "video", "order": sort_by, "maxResults": max_results}

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
            response = requests.get(base_url, params=params)
            response.raise_for_status()
        except requests.RequestException:
            print("An error occurred while making the API request.")
            break

        # Parse the JSON response
        data = response.json()
        items = data.get("items", [])
        suggestions.extend(items)

        # Check if there are more pages of results
        next_page_token = data.get("nextPageToken")
        if not next_page_token or len(suggestions) >= max_results:
            break

    # Extract the video titles and URLs from the response
    videos = []
    for video in suggestions:
        title = video["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
        videos.append({"title": title, "url": url})

    # Return the list of videos
    suggested_videos = []
    while True:
        # Select a random video
        video = random.choice(videos)

        # Check if the video is already in the list
        if video not in suggested_videos:
            # Open the video in the web browser
            webbrowser.open_new(video["url"])

            # Print the video URL and title
            print(video["title"] + " - " + video["url"])

            # Add the video to the list
            suggested_videos.append(video)
            break
        else:
            continue