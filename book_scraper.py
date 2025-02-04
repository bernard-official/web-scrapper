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
    
def parse_book_list(html):
    """Parse book list page and extract book URLs"""
    soup = BeautifulSoup(html, 'lxml')
    books = soup.find_all('article', class_='product_pod')
    return [BASE_URL + '/' + book.h3.a['href'] for book in books]

def parse_book_page(html):
    """Parse individual book page and extract details"""
    soup = BeautifulSoup(html, 'lxml')
    
    book = {
        'title': soup.find('h1').text.strip(),
        'price': soup.find('p', class_='price_color').text.strip(),
        'rating': soup.find('p', class_='star-rating')['class'][1],
        'stock': soup.find('p', class_='instock').text.strip(),
        'category': soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip(),
        'description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
    }