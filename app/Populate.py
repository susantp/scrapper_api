import math

from bs4 import BeautifulSoup

from app.Scrapper import Scrape


class Populate:
    def __init__(self, stream):
        self.ids = None
        self.stream = stream
        self.product_asin_id = None
        self.product_details = None
        self.product_title = None
        self.product_price = None
        self.product_description = None
        self.product_features = None
        self.product_information = None
        self.product_list = None
        self.product = None

    def pick_product_price(self):
        soup = BeautifulSoup(self.stream, "lxml")
        #
        return self.product_price

    def pick_product_title(self):
        soup = BeautifulSoup(self.stream, "lxml")
        el = soup.select_one("span#productTitle")

        if el is not None:
            self.product_title = el.text.strip()
            return self.product_title

        return self.product_title

    def pick_product_description(self):
        soup = BeautifulSoup(self.stream, "lxml")
        el = soup.select_one("div#productDescription")

        if el is not None:
            self.product_description = el.text.strip()
            return self.product_description

        return self.product_description

    def pick_product_features(self):
        features = dict()
        soup = BeautifulSoup(self.stream, "lxml")
        feature_bullets = soup.select("div#feature-bullets li", None, limit=10)

        if feature_bullets is not None:
            for count, item in enumerate(feature_bullets):
                features[count] = item.text.strip()
                self.product_features = features

        return self.product_features

    def pick_product_details(self):
        details = dict()
        soup = BeautifulSoup(self.stream, "lxml")
        product_details = soup.select("#detailBullets_feature_div > ul > li")

        if product_details is not None:
            for y in product_details:
                detail = y.text.split(":")
                key = detail[0].replace(" ", "").replace("•", "").replace("\n", "").replace("\u200f", "").strip()
                value = detail[1].replace(" ", "").replace("\n", "").replace("\u200e", "").strip()
                details[key] = value
                self.product_details = details

        return self.product_details

    def pick_product_information(self):
        information = dict()
        soup = BeautifulSoup(self.stream, "lxml")
        product_info_table = soup.select("#productDetails_detailBullets_sections1 > tr")

        if product_info_table is not None:
            for items in product_info_table:
                key = items.select_one("th").text.strip()
                value = items.select_one("td").text.strip()
                information[key] = value

        self.product_information = information
        return self.product_information

    def get_product(self, asin_id):
        self.stream = Scrape().crawl_page(asin_id)
        self.product = {
            "slug": asin_id,
            'title': self.pick_product_title(),
            'description': self.pick_product_description(),
            'features': self.pick_product_features(),
            'details': self.pick_product_details(),
        }
        return self.product

    def get_products(self, asin_ids, start_index=0, end_index=10):
        single_product = dict()
        for item in asin_ids:
            asin_id = asin_ids[item]['asin_id']
            price = asin_ids[item]['price']
            stream = Scrape().crawl_page(asin_id)

            single_product[asin_id] = {
                "slug": asin_id,
                'title': Populate(stream).pick_product_title(),
                'description': Populate(stream).pick_product_description(),
                'features': Populate(stream).pick_product_features(),
                'details': Populate(stream).pick_product_details(),
                'price': price
            }
            start_index += 1
            if start_index == end_index:
                break
        self.product_list = single_product
        return self.product_list

    def populate_ids_from_product_list_page(self):
        soup = BeautifulSoup(self.stream, "lxml")
        lists = soup.select("#ProductGrid-CdcDsKf > div > div > div > div > ul > li")
        ids = dict()
        for item in lists:
            anchor_el = item.select_one("div:nth-child(1) > a")
            price_el = item.select_one(
                "div.ProductGridItem__item__2jj5r.ProductGridItem__item-with-best-seller__2WzoC > div.ProductGridItem__itemInfo__s_dZ2 > div.ProductGridItem__itemInfoChild__1HpO6 > div.ProductGridItem__price__2H_kW > span")

            if (anchor_el is not None) and (price_el is not None):
                asin_id = anchor_el['href'].split("/")[-1].split('?')[0]
                price = price_el['aria-label'][1:].replace(",", "")
                ids[asin_id] = {"asin_id": asin_id, "price": math.floor(float(price) * 100)}

        self.ids = ids
        return self.ids
