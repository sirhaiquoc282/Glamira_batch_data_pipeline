import os
import csv


class DataCrawlingPipeline:
    def open_spider(self, spider):
        try:
            file_path = "../../../data/scrapy/products.csv"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file_exists = os.path.exists(file_path)
            self.file = open(file_path, "a", newline="", encoding="utf-8", buffering=1)
            fieldnames = ["product_id", "product_name"]
            self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
            if not file_exists:
                self.writer.writeheader()
        except Exception as e:
            spider.logger.error(f"Error opening file: {e}")
            raise e

    def process_item(self, item, spider):
        if "product_id" in item and "product_name" in item:
            try:
                self.writer.writerow(item)
                self.file.flush()
            except Exception as e:
                spider.logger.error(f"Error writing item {item}: {e}")
        else:
            spider.logger.warning(f"Item doesn't have enough specified fields: {item}")
        return item

    def close_spider(self, spider):
        try:
            if self.file:
                self.file.close()
        except Exception as e:
            spider.logger.error(f"Error closing file: {e}")
