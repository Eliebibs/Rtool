from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from gptApi import summarize_html  # Import the summarize_html function

app = Flask(__name__)
CORS(app)  # Enable CORS

def fetch_search_results(api_key, cse_id, query, num_results):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': num_results,
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_and_extract_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from specific tags
        text_elements = []
        for tag in ['title', 'h1', 'h2', 'h3', 'p']:
            for element in soup.find_all(tag):
                text_elements.append(element.get_text(strip=True))
        
        # Concatenate all text elements into a single string
        text_content = ' '.join(text_elements)
        return text_content
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return ""

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('research')
    api_key = 'AIzaSyBkr3Gs5TgIniWYavwaLfhdTp_XrLHUBqo'
    cse_id = '233652143b68349f5'
    
    results = fetch_search_results(api_key, cse_id, query, 5)
    links = [item['link'] for item in results.get('items', [])]
    
    search_results = {}
    for link in links:
        text_content = parse_and_extract_text(link)
        if text_content:
            summary = summarize_html(text_content)
            search_results[link] = summary
    
    return jsonify(search_results)

if __name__ == "__main__":
    app.run(debug=True)