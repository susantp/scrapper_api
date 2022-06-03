import math
import os

from bs4 import BeautifulSoup
import requests

# from app.main import static_path
static_path = os.path.join(os.path.dirname(__file__), 'static')


class Scrape:
    def __init__(self):
        self.file_path = None
        self.page_url = "http://api.scraperapi.com?api_key=dd424a4ae2c60473bb07132def3b89a1&url=https://www.amazon" \
                        ".com/dp/"
        self.stream = None
        self.message = None

    def crawl_page(self, asin_id):
        url = self.page_url + asin_id
        local_file_path = os.path.join(static_path, "product_page/" + asin_id)
        if not os.path.exists(local_file_path):
            self.stream = requests.get(url).text
            # write to file for second time not read from remote
            file = open(local_file_path, "w+")
            file.write(self.stream)
            file.close()
            # write end
            return self.stream
        return self.crawl_local_file(local_file_path)

    def crawl_local_file(self, file_path):
        file = open(file_path, "r")
        self.stream = file.read()
        file.close()
        return self.stream

    def read_url(self, asin_id):
        host = 'http://api.scraperapi.com'
        api_key = 'dd424a4ae2c60473bb07132def3b89a1'
        url = host + "?api_key=" + api_key + "&url=https://www.amazon.com/dp/" + asin_id

        if os.path.exists(os.path.join(static_path, "product_page/" + asin_id)):
            self.file_path = "product_page/" + asin_id
            return self.read_file(self.file_path)

        if not os.path.exists(os.path.join(static_path, "product_page/" + asin_id)):
            r = requests.get(url).text
            file = open(os.path.join(static_path, "product_page/" + asin_id), "w+")
            file.write(r)
            file.close()
            return r

    def get_stream(self):
        file_path = os.path.join(static_path, self.path)
        file = open(file_path, "r")
        self.stream = file.read()
        file.close()
        return self.stream

    def write_file(self, stream, file_name):
        file_path = os.path.join(static_path, "product_data", file_name + ".json")
        file = open(file_path, "w")
        file.write(stream)
        file.close()
        self.message = file_name + ".json created"
        return self.message


class Populate:

    def __init__(self):
        self.product_list = dict()
        self.product_title = None
        self.product_price = None
        self.product_description = None
        self.product_features = None
        self.product_details = None
        self.product_information = None

    def populate_info_from_product_list_page(self, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        lists = soup.select("#ProductGrid-CdcDsKf > div > div > div > div > ul > li")
        for item in lists:
            anchor_el = item.select_one("div:nth-child(1) > a")
            price_el = item.select_one(
                "div.ProductGridItem__item__2jj5r.ProductGridItem__item-with-best-seller__2WzoC > div.ProductGridItem__itemInfo__s_dZ2 > div.ProductGridItem__itemInfoChild__1HpO6 > div.ProductGridItem__price__2H_kW > span")
            if (anchor_el is not None) and (price_el is not None):
                asin_id = anchor_el['href'].split("/")[-1].split('?')[0]
                price = price_el['aria-label'][1:].replace(",", "")
                self.product_list[asin_id] = {"asin_id": asin_id, "price": math.floor(float(price) * 100)}

        return self.product_list

    def get_product_title(self, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        self.product_title = soup.select_one("span#productTitle").text.strip()
        return self.product_title

    def get_product_description(self, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        self.product_description = soup.select_one("div#productDescription").text.strip()
        return self.product_description

    def get_product_features(self, stream=""):
        features = dict()
        soup = BeautifulSoup(stream, "lxml")
        feature_bullets = soup.select("div#feature-bullets li", None, limit=10)
        for count, item in enumerate(feature_bullets):
            features[count] = item.text.strip()
        self.product_features = features
        return self.product_features

    def get_product_details(self, stream=""):
        details = dict()
        soup = BeautifulSoup(stream, "lxml")
        product_details = soup.select("#detailBullets_feature_div > ul > li")
        for y in product_details:
            s = []
            detail = y.text.split(":")
            key = detail[0].replace(" ", "").replace("•", "").replace("\n", "").replace("\u200f", "").strip()
            value = detail[1].replace(" ", "").replace("\n", "").replace("\u200e", "").strip()
            details[key] = value
        self.product_details = details
        return self.product_description

    def get_product_information(self, stream=""):
        information = dict()
        soup = BeautifulSoup(stream, "lxml")
        product_info_table = soup.select("#productDetails_detailBullets_sections1 > tr")
        for items in product_info_table:
            key = items.select_one("th").text.strip()
            value = items.select_one("td").text.strip()
            information[key] = value
        self.product_information = information
        return self.product_information
