from utils.logger import Logger
from utils.gcs_utils import GCSManager
from utils.type_converter import type_convertor
from utils.mongo_utils import MongoManager
import json
from typing import List, Tuple
from pathlib import Path


def extract_mongodb_to_gcs(
    logger,
    mongo_manager,
    gcs_manager,
    bucket_name,
    collections: List[Tuple[str, str]],
    base_path,
    batch_size,
):
    for db_name, collection_name in collections:
        checkpoint_path = f"{base_path}/{db_name}/{collection_name}/checkpoint.json"
        target_path = f"{base_path}/{db_name}/{collection_name}"

        try:
            last_id, part_number = gcs_manager.get_checkpoint(
                bucket_name, checkpoint_path
            )
            cursor = mongo_manager.get_collection_cursor(
                db_name, collection_name, last_id
            )
            batch = []
            for doc in cursor:
                doc = type_convertor(doc)
                batch.append(json.dumps(doc, default=str))
                last_id = doc["_id"]
                if len(batch) >= batch_size:
                    gcs_manager.upload_batch(
                        bucket_name, target_path, part_number, batch
                    )
                    part_number += 1
                    gcs_manager.save_checkpoint(
                        bucket_name, checkpoint_path, last_id, part_number
                    )
                    batch = []
            if batch:
                if gcs_manager.upload_batch(
                    bucket_name, target_path, batch, part_number
                ):
                    gcs_manager.save_checkpoint(
                        bucket_name, checkpoint_path, last_id, part_number + 1
                    )
                batch = []
        except Exception as e:
            logger.error(
                f"Failed to extract data from {db_name}.{collection_name} to GCS: {e}"
            )
            continue


if __name__ == "__main__":
    logger = Logger(name="mongodb_to_gcs")
    mongo_manager = MongoManager(logger, "mongodb://localhost:27017")
    gcs_manager = GCSManager(logger, "path/to/credential.json")
    bucket_name = "your_bucket_name"

    extract_mongodb_to_gcs(logger, mongo_manager, gcs_manager, bucket_name, [], 1000)
