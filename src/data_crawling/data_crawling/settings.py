import os

BOT_NAME = "data_crawling"

SPIDER_MODULES = ["data_crawling.spiders"]
NEWSPIDER_MODULE = "data_crawling.spiders"
MONGO_URI = "mongodb://admin:Nguyenhaiquoc13571790@34.142.175.171/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false"


ROBOTSTXT_OBEY = False
MONGO_URI = "mongodb://admin:Nguyenhaiquoc13571790@34.142.175.171/?authSource=admin"
MONGO_DATABASE = "countly"
COLLECTION_NAME = "summary"

LOG_DIR = "../../../logs/scrapy"
LOG_FILE = os.path.join(LOG_DIR, "scrapy.log")
os.makedirs(LOG_DIR, exist_ok=True)


CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = True
RETRY_TIMES = 5

DEFAULT_REQUEST_HEADERS = {
    "authority": "www.glamira.com.au",
    "method": "GET",
    "path": "/",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "cache-control": "no-store, no-cache, must-revalidate, max-age=0",
    "pragma": "cache",
    "referer": "https://www.glamira.com.au/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}
DEFAULT_COOKIES = {
    "mage-cache-storage": "{}",
    "mage-cache-storage-section-invalidation": "{}",
    "recently_viewed_product": "{}",
    "recently_viewed_product_previous": "{}",
    "recently_compared_product": "{}",
    "recently_compared_product_previous": "{}",
    "product_data_storage": "{}",
    "storage_content": "{}",
    "mage-messages": "",
    "sbjs_migrations": "1418474375998=1",
    "sbjs_current_add": "fd=2025-02-20 15:19:22|||ep=https://www.glamira.com.au/glamira-earring-louisa.html?alloy=white-585&diamond=diamond-sapphire|||rf=(none)",
    "sbjs_first_add": "fd=2025-02-20 15:19:22|||ep=https://www.glamira.com.au/glamira-earring-louisa.html?alloy=white-585&diamond=diamond-sapphire|||rf=(none)",
    "sbjs_current": "typ=typein|||src=(direct)|||mdm=(none)|||cmp=(none)|||cnt=(none)|||trm=(none)",
    "sbjs_first": "typ=typein|||src=(direct)|||mdm=(none)|||cmp=(none)|||cnt=(none)|||trm=(none)",
    "_gcl_au": "1.1.1589458333.1740039562",
    "form_key": "H9N8Wo7eSAjEvwrq",
    "PHPSESSID": "8ej2lnchculnb7uvcbqtc7oh82",
    "_fbp": "fb.2.1740039563471.14889595420232720",
    "sqzl_consent": "analytics,marketing",
    "sqzllocal": "sqzl67b6e58f000006081b80",
    "private_content_version": "24eb6fdd9389097a1e5f6721366ccb95",
    "scgacid": "1531812875.1740039561",
    "gagtmblock": "gab=0|||gtmb=0",
    "sqzl_vw": '{"2":{"c":1,"ex":1742631570},"9":{"c":1,"ex":1742631570}}',
    "bm_sz": "7BFA9ABEC0B7A6434D3F836D6CBC04F2~YAAQv9ocuJ2i/6SVAQAA/ELBrRv4L4Xk31rrfbL9haoXT/6H0+gwang45CSkFgNh9f8E3GyU/T5vOPIZOaaWtS+zNCpc2n6A1rwQ0ZixyZNzp830WUI8WLUaKn2VUc9dWDQeWNo+YJSRtAI89NP1h8dYYSIY4CwA808Nd7d4PyIYxbsVGMedYzJUe29qDuw/LEZqU3xs1U3IGpy1kRwkD53jNeudJnHBPyIR0VziQxQzfly4ZMf7N+r+fTBZliLyDoFCReHscFk8mDg4joZyWOFrf61X0NegI5412mxtwubYrmNHxhvqEf4PO3gFG28vXBqNSosXbFWCzvioKuY9ZEwdCeYmBjLp0af9vQZJ8A/hiiwf4W38HA+RLMLU/hUl5NWNohBTjLBEK7ptZ77EjnA=~3359540~4405045",
    "_gid": "GA1.3.1183290632.1742376880",
    "_gat_gtag_UA_55554914_1": "1",
    "_abck": "9E2B6E3B86E918E24ACEBD46AE93E7C1~0~YAAQv9ocuKGi/6SVAQAAP0rBrQ05DESnAIuS2x/i7BswCWEIY0ZVB8ZcR6oUa9YewVK/yePRyfPJTGi3ru1boN105PFWg2Gv3H/jkh5VvfKDzfSAng3bvAZFHQfJwD37AjdwtJLfa4EK9lZ3JBtfGAP4ShGZwB3ltpFvjSd8/C6OEznKfeaqi...",
}

ITEM_PIPELINES = {
    "data_crawling.pipelines.DataCrawlingPipeline": 300,
}
HTTPCACHE_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
