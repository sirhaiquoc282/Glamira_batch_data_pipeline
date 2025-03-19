import scrapy
import pymongo
from scrapy.exceptions import IgnoreRequest
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
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE]
        self.collection_name = COLLECTION_NAME

    def start_requests(self):
        cursor = self.db[self.collection_name].find({})
        for doc in cursor:
            product_id = doc.get("product_id")
            current_url = doc.get("current_url")

            if not product_id or not current_url:
                continue

            yield scrapy.Request(
                url=current_url,
                headers=DEFAULT_REQUEST_HEADERS,
                cookies=DEFAULT_COOKIES,
                callback=self.parse,
                errback=self.handle_error,
                meta={
                    "product_id": product_id,
                    "retry_count": 0,
                },  # ✅ Thêm retry_count
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

        if status in (500, 502, 503, 504, 408) or failure.check(
            DNSLookupError, TimeoutError, TCPTimedOutError
        ):
            if retry_count < RETRY_TIMES:
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
