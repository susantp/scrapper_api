import math
import os.path
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from app.Scrapper import Scrape
from comment import main as comment_main, schemas
from app.config import settings
from app.database import engine

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="description",
    version="0.0.1",
    terms_of_service="tos",
    contact={
        "name": "Susant",
        "url": "http://www.susantpaudel.com.np",
        "email": "gracysusant@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/openapi.json"
)
static_path = os.path.join(os.path.dirname(__file__), 'static')
scrap_api_token = settings.scrap_api_token
# app.mount("static", StaticFiles(directory="static"), name="static")

#
# class Scrape:
#
#     @classmethod
#     def read_url(cls, asin_id):
#         host = 'http://api.scraperapi.com'
#         api_key = 'dd424a4ae2c60473bb07132def3b89a1'
#         url = host + "?api_key=" + api_key + "&url=https://www.amazon.com/dp/" + asin_id
#
#         if os.path.exists(os.path.join(static_path, "product_page/" + asin_id)):
#             return cls.read_file("product_page/" + asin_id)
#
#         if not os.path.exists(os.path.join(static_path, "product_page/" + asin_id)):
#             r = requests.get(url).text
#             file = open(os.path.join(static_path, "product_page/" + asin_id), "w+")
#             file.write(r)
#             file.close()
#             return r
#
#     @classmethod
#     def read_file(cls, file=""):
#         file_path = os.path.join(static_path, file)
#         file = open(file_path, "r")
#         stream = file.read()
#         file.close()
#         return stream
#
#     @classmethod
#     def write_file(cls, stream, file_name):
#         file_path = os.path.join(static_path, "product_data", file_name + ".json")
#         file = open(file_path, "w")
#         file.write(stream)
#         file.close()
#         return file_name + ".json created"


class Populate:
    @classmethod
    def populate_info_from_product_list_page(cls, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        lists = soup.select("#ProductGrid-CdcDsKf > div > div > div > div > ul > li")
        info = dict()
        for item in lists:
            anchor_el = item.select_one("div:nth-child(1) > a")
            price_el = item.select_one(
                "div.ProductGridItem__item__2jj5r.ProductGridItem__item-with-best-seller__2WzoC > div.ProductGridItem__itemInfo__s_dZ2 > div.ProductGridItem__itemInfoChild__1HpO6 > div.ProductGridItem__price__2H_kW > span")
            if (anchor_el is not None) and (price_el is not None):
                asin_id = anchor_el['href'].split("/")[-1].split('?')[0]
                price = price_el['aria-label'][1:].replace(",", "")
                info[asin_id] = {"asin_id": asin_id, "price": math.floor(float(price) * 100)}

        return info

    @classmethod
    def product_price(cls, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        return ''

    @classmethod
    def product_title(cls, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        return soup.select_one("span#productTitle").text.strip()

    @classmethod
    def product_description(cls, stream=""):
        soup = BeautifulSoup(stream, "lxml")
        return soup.select_one("div#productDescription").text.strip()

    @classmethod
    def product_features(cls, stream=""):
        features = dict()
        soup = BeautifulSoup(stream, "lxml")
        feature_bullets = soup.select("div#feature-bullets li", None, limit=10)
        for count, item in enumerate(feature_bullets):
            features[count] = item.text.strip()
        return features

    @classmethod
    def product_details(cls, stream=""):
        details = dict()
        soup = BeautifulSoup(stream, "lxml")
        product_details = soup.select("#detailBullets_feature_div > ul > li")
        for y in product_details:
            s = []
            detail = y.text.split(":")
            key = detail[0].replace(" ", "").replace("•", "").replace("\n", "").replace("\u200f", "").strip()
            value = detail[1].replace(" ", "").replace("\n", "").replace("\u200e", "").strip()
            details[key] = value
        return details

    @classmethod
    def product_information(cls, stream=""):
        information = dict()
        soup = BeautifulSoup(stream, "lxml")
        product_info_table = soup.select("#productDetails_detailBullets_sections1 > tr")
        for items in product_info_table:
            key = items.select_one("th").text.strip()
            value = items.select_one("td").text.strip()
            information[key] = value
        return information


@app.get('/scrap_page/{asin_id}')
async def scrap_page(asin_id=""):
    if not len(asin_id) > 0:
        return {"message": "please provide asin id"}
    return Scrape().crawl_page(asin_id)


@app.get('/')
async def home():
    product_dict = dict()
    # file_path = "product_page/B00SR7YXB0"
    file_path = "product_list_page/list.html"
    stream = Scrape(file_path).read_url()
    ids = Populate().populate_info_from_product_list_page(stream)
    i = 0
    single_product = dict()
    for item in ids:
        asin_id = ids[item]['asin_id']
        price = ids[item]['price']
        stream = Scrape().read_url(asin_id)
        single_product[asin_id] = {
            "slug": asin_id,
            'title': Populate().product_title(stream),
            'description': Populate().product_description(stream),
            'features': Populate().product_features(stream),
            'details': Populate().product_details(stream),
            'price': price
        }
        i += 1
        if i == 10:
            break
    product_dict = single_product

    return product_dict


app.include_router(comment_main.router)
