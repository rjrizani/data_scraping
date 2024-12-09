import datetime

import pandas as pd
import requests
from .soup import Soup

import sqlite3
from src.models import BookSQL


def get_html(url: str) -> str:
    r = requests.get(url)
    return r.text
    #return Soup(r.text)

def save_to_xlsx(data) -> None:
    df = pd.DataFrame(data)
    current_date = datetime.date.today().strftime("%Y_%m_%d")
    filename = f"books_{current_date}.xlsx"
    df.to_excel(filename, index=False)

    print(f"Data saved to {filename}")


def save_to_db(data: list) -> None:
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    for book in data:
        cursor.execute('''
            INSERT INTO books (title, price, stock, rating, description, url, product_type, product_incl_tax, product_excl_tax, tax, total_reviews, img_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            book.title,
            book.price,
            book.stock,
            book.rating,
            book.description,
            book.url,
            book.product_type,
            book.product_incl_tax,
            book.product_excl_tax,
            book.tax,
            book.total_reviews,
            book.img_url
        ))

    conn.commit()
    conn.close()
    print("Data saved to database sqllite")