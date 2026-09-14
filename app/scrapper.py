import os
import re
from pathlib import Path

import requests

from app.config import settings

STATIC_PATH = Path(__file__).resolve().parent / "static"
ASIN_PATTERN = r"^[A-Z0-9]{10}$"


class Scrape:
    def __init__(self):
        self.local_file_path = None
        self.page_url = "https://api.scraperapi.com"
        self.stream = None
        self.message = None

    def crawl_page(self, asin_id, background_tasks=None):
        url = f"https://www.amazon.com/dp/{asin_id}"
        self.get_local_file_path_by_asin_id(asin_id)
        if not os.path.exists(self.local_file_path):
            self.get_stream_remote(url)
            if background_tasks is not None:
                background_tasks.add_task(self.write_stream_to_file)
                return self.stream
            self.write_stream_to_file()
            return self.stream

        return self.get_stream_local(self.local_file_path)

    def get_stream_remote(self, url):
        if not settings.scrap_api_token:
            raise RuntimeError("SCRAP_API_TOKEN is not configured")

        response = requests.get(
            self.page_url,
            params={"api_key": settings.scrap_api_token, "url": url},
            timeout=30,
        )
        response.raise_for_status()
        self.stream = response.text
        return self.stream

    def get_stream_local(self, file_path):
        file_path = self.get_local_file_path_by_path(file_path)
        with file_path.open("r", encoding="utf-8") as file:
            self.stream = file.read()
        return self.stream

    # utilities #

    def write_stream_to_file(self):
        self.local_file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.local_file_path.open("w", encoding="utf-8") as file:
            file.write(self.stream or "")

    def get_local_file_path_by_path(self, path):
        normalized_path = (STATIC_PATH / path).resolve()
        if os.path.commonpath((STATIC_PATH, normalized_path)) != str(STATIC_PATH):
            raise ValueError("Invalid path")
        self.local_file_path = normalized_path
        return self.local_file_path

    def get_local_file_path_by_asin_id(self, asin_id):
        if not asin_id or not re.fullmatch(ASIN_PATTERN, asin_id):
            raise ValueError("Invalid ASIN")
        normalized_path = (STATIC_PATH / "product_page" / asin_id).resolve()
        if os.path.commonpath((STATIC_PATH, normalized_path)) != str(STATIC_PATH):
            raise ValueError("Invalid path")
        self.local_file_path = normalized_path
        return self.local_file_path
