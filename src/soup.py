from bs4 import BeautifulSoup
from .models import Book
from src import BASE_URL

class Soup(BeautifulSoup):

    def __init__(self, html) -> None:
        super().__init__(html, 'html.parser')
        self.url = BASE_URL


    def scrape(self) -> None:
        title = self.find("div", {"class": "product_main"}).find("h1").get_text()
        price = float(self.find("p", {"class": "price_color"}).get_text().removeprefix("Â£"))
        stock = int((self.find("p", class_="instock availability").get_text().strip()
                 .replace("In stock (", "").replace(" available)", "")))
        rating = self.find("p", class_="star-rating").get_attribute_list("class")[1]
        rating = self.convert_rating(rating)

        article = self.find("article", class_="product_page")
        desc_element = article.find("p", class_=False, id=False) if article else None
        description = desc_element.get_text() if desc_element else ""
        
        table :list[BeautifulSoup] = self.find("table", class_="table table-striped").findAll("td")
        table = [t.get_text() for t in table]
        upc = table[0]
        product_type = table[1]
        product_incl_tax = float(table[2].replace("Â£", "").replace(",", ""))
        product_excl_tax = float(table[3].replace("Â£", "").replace(",", ""))
        tax = float(table[4].replace("Â£", "").replace(",", ""))
        total_reviews = int(table[-1])
        img_url = self.find("img")["src"].replace("../../", BASE_URL)

        return Book(title,
                    price,
                    stock,
                    rating,
                    description,
                    upc, product_type,
                    product_incl_tax,
                    product_excl_tax,
                    tax,
                    total_reviews,
                    img_url)

    def scrape_urls(self):
        elements = self.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        product_urls = []
        for element in elements:
            # Find the anchor tag within the element
            anchor_element = element.find("a")
            if anchor_element:
                # Get the URL from the href attribute
                product_url = anchor_element["href"].replace("../../", f"{BASE_URL}catalogue/")
                product_urls.append(product_url)
        return product_urls

    #get max pafe
    def get_max_page(self):
        max_page = int(self.find("li", class_="current").find("a").get_text())
        return max_page
    def convert_rating(self, rating :str) -> int:
        match rating:
            case "One":
                return 1
            case "Two":
                return 2
            case "Three":
                return 3
            case "Four":
                return 4
            case "Five":
                return 5
            case _:
                return 0

