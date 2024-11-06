import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape images from Bing based on a query
def scrape_images(query):
    query = query.replace(" ", "+")  # Format the query for the URL
    url = f"https://www.bing.com/images/search?q={query}"  # Bing Image Search URL
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send the GET request to Bing
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all image tags and collect their src attributes
    image_urls = []
    img_tags = soup.find_all("img")
    for img in img_tags:
        img_url = img.get("src")
        if img_url and img_url.startswith("http"):
            image_urls.append(img_url)
    
    return image_urls

@app.route("/", methods=["GET", "POST"])
def home():
    images = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query")  # Get the search query from the form
        if query:
            images = scrape_images(query)  # Call the function to scrape images

    return render_template("index.html", images=images, query=query)

if __name__ == "__main__":
    app.run(debug=True)
