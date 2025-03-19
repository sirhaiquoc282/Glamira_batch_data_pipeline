import scrapy
from pymongo import MongoClient
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from data_crawling.settings import (
    DEFAULT_REQUEST_HEADERS,
    DEFAULT_COOKIES,
    RETRY_TIMES,
    MONGO_URI,
    MONGO_DATABASE,
    COLLECTION_NAME,
)


class GlamiraSpider(scrapy.Spider):
    name = "glamira"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection_name = COLLECTION_NAME
        self.mongo_uri = MONGO_URI
        self.mongo_database = MONGO_DATABASE
        self.default_request_headers = DEFAULT_REQUEST_HEADERS
        self.default_cookies = DEFAULT_COOKIES
        self.retry_times = RETRY_TIMES
        self.client = self.get_connection()

    def get_connection(self):
        try:
            client = MongoClient(self.mongo_uri)
            client.admin.command("ping")
            self.logger.info("Connected to MongoDB")
            return client
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_url(self):
        try:
            pipeline = [
                {
                    "$match": {
                        "collection": {
                            "$in": [
                                "view_product_detail",
                                "select_product_option",
                                "select_product_option_quality",
                            ]
                        }
                    }
                },
                {"$project": {"_id": 0, "product_id": 1, "current_url": 1}},
            ]
            cursor = self.client[self.mongo_database][self.collection_name].aggregate(
                pipeline
            )
            self.logger.info("Fetched url from MongoDB")
            return cursor
        except Exception as e:
            self.logger.error(f"Failed to fetch url from MongoDB: {e}")
            raise

    def start_requests(self):
        cursor = self.get_url()
        for doc in cursor:
            product_id = doc.get("product_id")
            current_url = doc.get("current_url")

            if not product_id or not current_url:
                continue

            yield scrapy.Request(
                url=current_url,
                headers=self.default_request_headers,
                cookies=self.default_cookies,
                callback=self.parse,
                errback=self.handle_error,
                meta={
                    "product_id": product_id,
                    "retry_count": 0,
                },
            )

    def parse(self, response):
        product_id = response.meta["product_id"]
        product_name = response.xpath(
            '//*[@id="maincontent"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/h1/span/text()'
        ).get()
        yield {"product_id": product_id, "product_name": product_name}

    def handle_error(self, failure):
        request = failure.request
        retry_count = request.meta.get("retry_count", 0)
        status = failure.value.response.status if failure.check(HttpError) else None

        if status in (500, 502, 503, 504, 408, 429) or failure.check(
            DNSLookupError, TimeoutError, TCPTimedOutError
        ):
            if retry_count < self.retry_times:
                retry_count += 1
                self.logger.warning(f"Retrying {request.url} (retry {retry_count})")
                retry_request = request.copy()
                retry_request.meta["retry_count"] = retry_count
                yield retry_request
            else:
                self.logger.info(f"Retry limit reached for {request.url}, skipping")
                return
        else:
            self.logger.error(f"Error {status} on {request.url}")
            return
