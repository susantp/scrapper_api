import os.path

from fastapi import FastAPI

from app.Populate import Populate
from app.Scrapper import Scrape
from app.config import settings
from app.database import engine
from comment import schemas

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
scrap_api_token = settings.scrap_api_token


@app.get('/scrap_page/{asin_id}')
async def scrap_page(asin_id=""):
    if not len(asin_id) > 0:
        return {"message": "please provide asin id"}
    stream = Scrape().crawl_page(asin_id)
    return Populate(stream).get_product(asin_id)


@app.get('/get_product_list')
async def scrap_list():
    list_path = "product_list_page/list.html"
    stream = Scrape().get_stream_local(list_path)
    ids = Populate(stream).populate_ids_from_product_list_page()
    products = Populate(stream).get_products(ids, 0, 3)
    return products


@app.get('/')
async def home():
    return "here"
    return {"welcome"}

# app.include_router(comment_main.router)
