import os

import requests
static_path = os.path.join(os.path.dirname(__file__), 'static')


class Scrape:
    def __init__(self):
        self.local_file_path = None
        self.page_url = "http://api.scraperapi.com?api_key=api_key&url=https://www.amazon" \
                        ".com/dp/"
        self.stream = None
        self.message = None

    def crawl_page(self, asin_id, background_tasks=None):  # check if file exists locally, craws local else crawl remote page url
        url = self.page_url + asin_id
        self.get_local_file_path_by_asin_id(asin_id)
        ss = background_tasks
        if not os.path.exists(self.local_file_path):
            self.get_stream_remote(url)
            if background_tasks is not None:
                background_tasks.add_task(self.write_stream_to_file())
            else:
                self.write_stream_to_file()
                return self.stream

        return self.get_stream_local(self.local_file_path)

    def get_stream_remote(self, url):
        self.stream = requests.get(url).text
        return self.stream

    def get_stream_local(self, file_path):
        file_path = self.get_local_file_path_by_path(file_path)
        # if not file_path:
        #     # self.message
        #     return
        file = open(file_path, "r")
        self.stream = file.read()
        file.close()
        return self.stream

    # utilities #

    def write_stream_to_file(self):
        file = open(self.local_file_path, "w+")
        file.write(self.stream)
        file.close()
        pass

    def get_local_file_path_by_path(self, path):
        self.local_file_path = os.path.join(static_path, path)
        return self.local_file_path

    def get_local_file_path_by_asin_id(self, asin_id):
        self.local_file_path = os.path.join(static_path, "product_page/" + asin_id)
        return self.local_file_path
