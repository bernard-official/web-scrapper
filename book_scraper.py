import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randint

# Configuration
BASE_URL = "http://books.toscrape.com"
CSV_FILE = "books.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_page(url):
    """Fetch a web page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
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
    
    # Convert rating to numerical value
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    book['rating'] = rating_map.get(book['rating'], 0)
    
    return book

def save_to_csv(data, filename):
    """Save scraped data to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    all_books = []
    page_num = 1
    
    while True:
        print(f"Scraping page {page_num}...")
        url = f"{BASE_URL}/catalogue/page-{page_num}.html"
        html = get_page(url)
        
        if not html:
            break
            
        book_urls = parse_book_list(html)
        
        for book_url in book_urls:
            print(f"Scraping {book_url}")
            book_html = get_page(book_url)
            if book_html:
                book_data = parse_book_page(book_html)
                all_books.append(book_data)
                sleep(randint(1, 3))  # Be polite with delays
            
        # Check if next page exists
        soup = BeautifulSoup(html, 'lxml')
        next_button = soup.find('li', class_='next')
        if not next_button:
            break
            
        page_num += 1
    
    if all_books:
        save_to_csv(all_books, CSV_FILE)
        print(f"Scraped {len(all_books)} books. Data saved to {CSV_FILE}")
    else:
        print("No books scraped")

if __name__ == "__main__":
    main()