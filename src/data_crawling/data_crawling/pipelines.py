import csv
import os


class DataCrawlingPipeline:
    def open_spider(self, spider):
        file_path = "../../../data/scrapy/products.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_exists = os.path.exists(file_path)
        self.file = open(file_path, "a", newline="", encoding="utf-8")
        fieldnames = ["product_id", "product_name"]
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        if not file_exists:
            self.writer.writeheader()

    def process_item(self, item, spider):
        if "product_id" in item and "product_name" in item:
            self.writer.writerow(item)
        else:
            spider.logger.warning(f"Item doesn't have enough specified fields: {item}")
        return item

    def close_spider(self, spider):
        self.file.close()
