import os
import logging

BOT_NAME = "data_crawling"

SPIDER_MODULES = ["data_crawling.spiders"]
NEWSPIDER_MODULE = "data_crawling.spiders"


ROBOTSTXT_OBEY = False
MONGO_URI = "mongodb://admin:Nguyenhaiquoc13571790@34.142.175.171/?authSource=admin"
MONGO_DATABASE = "countly"
COLLECTION_NAME = "summary"

LOG_DIR = "../../../logs/scrapy"
LOG_FILE = os.path.join(LOG_DIR, "scrapy.log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_LEVEL = logging.INFO


CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = True
RETRY_TIMES = 5

DEFAULT_REQUEST_HEADERS = {
    "authority": "www.glamira.com.au",
    "method": "GET",
    "path": "/",
    "scheme": "https",
    "referer": "https://www.glamira.com.au/",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "priority": "u=0, i",
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
    "sbjs_migrations": "1418474375998%3D1",
    "sbjs_current_add": "fd%3D2025-02-20%2015%3A19%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.glamira.com.au%2Fglamira-earring-louisa.html%3Falloy%3Dwhite-585%26diamond%3Ddiamond-sapphire%7C%7C%7Crf%3D%28none%29",
    "sbjs_first_add": "fd%3D2025-02-20%2015%3A19%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.glamira.com.au%2Fglamira-earring-louisa.html%3Falloy%3Dwhite-585%26diamond%3Ddiamond-sapphire%7C%7C%7Crf%3D%28none%29",
    "sbjs_current": "typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
    "sbjs_first": "typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
    "_gcl_au": "1.1.1589458333.1740039562",
    "form_key": "H9N8Wo7eSAjEvwrq",
    "PHPSESSID": "8ej2lnchculnb7uvcbqtc7oh82",
    "_fbp": "fb.2.1740039563471.14889595420232720",
    "sqzl_consent": "analytics%2Cmarketing",
    "sqzllocal": "sqzl67b6e58f000006081b80",
    "scgacid": "1531812875.1740039561",
    "gagtmblock": "gab=0|||gtmb=0",
    "sqzl_vw": "%7B%222%22%3A%7B%22c%22%3A1%2C%22ex%22%3A1742631570%7D%2C%229%22%3A%7B%22c%22%3A1%2C%22ex%22%3A1742631570%7D%7D",
    "_gid": "GA1.3.1183290632.1742376880",
    "mage-cache-sessid": "true",
    "bm_sz": "40AC276245CEED129982094AD6110416~YAAQpSUtFwTFja6VAQAA8QkirxujypVF8Ypq9PY8txWqi38CSDF8bMuN0PZgveexVZMUti0vRsVSqDLiJqHrH4WJTEmOWaF9unbPqISlfdn+VM3/1t5MzhBbqfGk0tug5YXzKSt/7xhB2J55xtlBUc8T3VgiYtfhR6QmkevpCEhWGx5fKzP0TOiDoY7upSf3bDCaBCWWncCL30g+tNTegLIaxCoL5X95fr4We29fJ/E0N06TuamWCuiFoWGJmgjOCh3d6UULqrBe4hKItwk1kQ2Me33yoohz640FhWDbDYPViaaNE6tZ2yt0FNohm66NmuqSixcuhIW0kqtJnDSYsqBnl2F2RnFtEClOX6LWhwKAAh+CiZokkSeGqCVwLVskGb0ROV0q2nR2ZbhDHwPxSzc=~4408120~4469826",
    "_gat_gtag_UA_55554914_1": "1",
    "_abck": "9E2B6E3B86E918E24ACEBD46AE93E7C1~0~YAAQpSUtF2rFja6VAQAAuQsirw0sc9Qr7r+3b02QxlppyFpkO90v1/I5qLaH3ng4GU6/BD3dHxiqwqCjDRQbg7MjTTF5hBmsUzvVxvxPtuJDPHIEKLmEppuXRCJe8DkA5Zk2bq+C3DlQUc7i2irAKYCtcEmrjC9afY0xddoSQaYOCRiCKBvhLkg37HnKZ/tn6DcfhuY+k9p6JhPDvZWOEwgs6+pxjsQXfee9gr4GkmqaKV49oEHACeKuy2kIWEr/3F62RLeY411V6MdeXpE5A2E1ld7oB1t4AEF+K0xb69ox6p8tbW79n0osMFYm+2/bU0ocR1i0zPSNjJU/NoWiOVP5nP/JNqq1M3pjNvQTIjHAhYp60zt+ohbLAurUWQYkg0BoVzaH97BTn2IdVf1furQJ30qpg7YRscAYrejdo+parB8oczETZOKr7lD42q7zu/booKL9S43pNDhR+kopkwLnDcAUksPvOrbaX8EoHp/v+OW1kQwtNvZ1wnLcFGSRi7iGzd8p4u2rMTdtZDcsyQmulqz4IxbhtGvQ/P0/n3Hp~-1~-1~-1",
    "sbjs_udata": "vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20Safari%2F537.36%20Edg%2F134.0.0.0",
    "sbjs_session": "pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.glamira.com.au%2Fglamira-ring-lytop.html%3Falloy%3Dwhite-platin%26stone1%3Dbrowndiamond",
    "sc_lurl": "/glamira-ring-lytop.html",
    "_gat_UA-55554914-1": "1",
    "_uetsid": "61d21de004a511f096b48175d2ac01c6|qw2bt|2|fuc|0|1904",
    "_ga": "GA1.1.1531812875.1740039561",
    "_ga_EBLPEHMQT3": "GS1.1.1742399999.5.0.1742399999.60.0.0",
    "_ga_K6SPNS0HQ9": "GS1.1.1742399999.5.0.1742399999.60.0.0",
    "private_content_version": "c4c787fc0bd07649d0933779a102525d",
    "ak_bmsc": "085D2694A5B48BA737A410844E0CDDE5~000000000000000000000000000000~YAAQpSUtFynHja6VAQAAhxMirxvb/fHVh8s3BSoKgU6UrzjPaoPO8SmBIDY+Y9e1kj/dt8E0I9ClolTZd8uW/Y8u9HkVji0bFAx8azS8UmypVMhxXflLJH98jtIH6RBaCr/y1C1PSR+xdniglUr1PZ+PhbhiWdt86MdRsyIGNn+slMIWfGme1561ulgzSHIi8EGhOrSbX0HZ/5koN7M5cXy7t6391EpUFs5jc0mnnnWoKnFPMJ+NvmI9mm0ASkLLLkMULpKSQASo+3U8419tqLcy4yOVGh93cv76NSnt0NtFKNYv/3DfP/yaTIK0J8qoclD0bU3Nd+JnIQ5Vpp+p/bGLEwLI1YsZgbCCrS1AQ4xdlRgq6ShqyEJoOJzz6X0sP1u3xZwxflQ2LIQCnyCq14ougUfhlI7hCxLYOi3ACzKzRoonClLfVpXHzFdaFhh9igVYIWbWlEaQdw==",
    "bm_sv": "CE2658EE8796519832333C57637969CB~YAAQpSUtF0PHja6VAQAA/BMirxvDmhKsljuaP29HEim5GsO0tKD0jGnZC267jo5HyhlXD5dEZT5Jznuwz7zM5a1LmRUERzg8Z0hYqN/W3biDtIc6d1B6DXMXYqyV1e2VVs7Ggt9+MJvTx3o+OijveMZfbc2fKfUgD0f2HGIUkZp/T/Y2e1+d5g91AkbFXe3i0zWubfV02ZjRmeP+G6cIXuxgWrW769Aknd6jBfuNpFRG5w/e1FoRqErxhxFHVamlNq2T2Q==~1",
    "_uetvid": "63c967a0ef6311efb8658b0ef320fc3a|1xrjlg1|1742400000746|1|1|bat.bing.com/p/insights/c/f",
    "cto_bundle": "6diYwV9NQVk2RkNZWk5uUmpGQ0RRTEhXdXVKRlRMdHB3JTJCZXlrMEZJdWJtJTJCam16aDlpd2hnWE4wQTBTN25aY0hiSDdpbGhMd2Z6Qks0QTRkSXY3SFlKOEFHT2ptcjJHdndBODVUbnd2OSUyRmplenZjY1RLZGpQWHdCYnhSbVVSU2g4YU9lQ1F1WWpIZ0VHaTRlVmtMRUtBREdTblhKS0E3d3VGMFJKMTdtZ1BBbld3TjlkblhLcHZCdCUyQjJOQllGbmFNRVY5Mg",
}

ITEM_PIPELINES = {
    "data_crawling.pipelines.DataCrawlingPipeline": 300,
}
HTTPCACHE_ENABLED = True

COOKIES_ENABLED = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
