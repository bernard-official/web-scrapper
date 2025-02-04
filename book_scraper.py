import requests
from bs4 import BeautifulSoup
import csv
import time from sleep
from random import randint 

# Configuration
BASE_URL = "http://books.toscrape.com"
CSV_FILE = "books.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_page(url):
    """Fetch the web page"""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None