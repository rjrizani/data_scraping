import datetime
import json
import pandas as pd

import requests
from bs4 import BeautifulSoup
from src.utils import get_html, save_to_db, save_to_xlsx
from src.soup import Soup

import time
from concurrent.futures import ThreadPoolExecutor


def scrape_book(url, page):
    html = get_html(url)
    soup = Soup(html)
    print(url, "scraped in page {}".format(page))
    return soup.scrape()

def acess_url_per_page() -> None:
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    html = get_html(url)
    soup = Soup(html)
    print(soup.scrape_urls())

#loop for each page to get url saved in list
def access_pages() -> None:
    base_url = "https://books.toscrape.com/catalogue/category/books_1/page-{}.html"
    for i in range(1, 51):  # assuming there are 50 pages
        url = base_url.format(i)
        html = get_html(url)
        soup = Soup(html)
        print(soup.scrape_urls())

def main():
    books = []  # Initialize an empty list to store scraped data
    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = []
        # Loop through the pages to get the list of book URLs
        for i in range(1, 50):
            page_url = f"https://books.toscrape.com/catalogue/category/books_1/page-{i}.html"
            html = get_html(page_url)
            soup = Soup(html)
            urls = soup.scrape_urls()
            # Schedule scraping each book concurrently
            for url in urls:
                futures.append(executor.submit(scrape_book, url, i))
                
        # Collect results from the futures
        for future in futures:
            books.append(future.result())


    # Save data to Excel file
    save_to_xlsx(books)

    #save to db sqllite
    save_to_db(books)


if __name__ == "__main__":
    main()
