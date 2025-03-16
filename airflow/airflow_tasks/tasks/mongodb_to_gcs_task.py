import json
from typing import List, Tuple
import argparse
import logging
from pathlib import Path

from utils.mongo_utils import MongoManager
from utils.gcs_utils import GCSManager
from utils.logger import Logger
from utils.type_converter import type_convertor
from configs.settings import (
    MONGO_URI,
    DB_COLLECTIONS,
    LOG_FILE,
    LOG_LEVEL,
    LOG_NAME,
    BATCH_SIZE,
    BUCKET_NAME,
    CREDENTIAL_PATH,
    BASE_PATH,
    log_levels,
)


def export_mongodb_collections(
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
        target_path = f"{base_path}/{db_name}/{collection_name}/{collection_name}"

        try:
            last_id, part_number = gcs_manager.load_checkpoint(
                bucket_name, checkpoint_path
            )
            cursor = mongo_manager.get_collection_cursor(
                db_name, collection_name, last_id
            )

            batch = []
            last_doc_id = None
            for doc in cursor:
                doc = type_convertor(doc)
                batch.append(json.dumps(doc, default=str))
                last_doc_id = doc["_id"]
                if len(batch) >= batch_size:
                    if gcs_manager.upload_batch(
                        bucket_name, target_path, batch, part_number
                    ):
                        part_number += 1
                        gcs_manager.save_checkpoint(
                            bucket_name, checkpoint_path, last_doc_id, part_number
                        )
                        batch = []

            if batch:
                if gcs_manager.upload_batch(
                    bucket_name, target_path, batch, part_number
                ):
                    gcs_manager.save_checkpoint(
                        bucket_name, checkpoint_path, last_doc_id, part_number + 1
                    )

        except Exception as e:
            logger.error(f"Failure to export for {db_name}.{collection_name}: {e}")
            continue


def parse_collections(raw_collections):
    return [tuple(pair.split(":")) for pair in raw_collections if ":" in pair]


def main():
    parser = argparse.ArgumentParser(description="MongoDB to GCS Export")
    parser.add_argument(
        "--mongo_uri", type=str, default=MONGO_URI, help="MongoDB connection URI"
    )
    parser.add_argument(
        "--db_collections",
        type=str,
        nargs="+",
        default=DB_COLLECTIONS,
        help="List of 'db:collection' pairs to export from MongoDB",
    )
    parser.add_argument(
        "--bucket_name", type=str, default=BUCKET_NAME, help="GCS bucket name"
    )
    parser.add_argument(
        "--base_path",
        type=str,
        default=BASE_PATH,
        help="Base path in GCS for uploaded data",
    )
    parser.add_argument(
        "--log_file", type=str, default=LOG_FILE, help="Path to log file"
    )
    parser.add_argument(
        "--log_level", type=str, default=LOG_LEVEL, help="Logging level"
    )
    parser.add_argument("--log_name", type=str, default=LOG_NAME, help="Logger name")
    parser.add_argument(
        "--batch_size", type=int, default=BATCH_SIZE, help="Size of each chunk"
    )
    parser.add_argument(
        "--credential_path",
        type=str,
        default=CREDENTIAL_PATH,
        help="Path to credential file",
    )
    args = parser.parse_args()

    try:
        logger = Logger(
            name=args.log_name,
            log_file=args.log_file,
            log_level=log_levels.get(args.log_level.lower(), logging.INFO),
        )
        mongo_manager = MongoManager(logger, args.mongo_uri)
        gcs_manager = GCSManager(logger, args.credential_path)

        collections = parse_collections(args.db_collections)
        export_mongodb_collections(
            logger,
            mongo_manager,
            gcs_manager,
            args.bucket_name,
            collections,
            args.base_path,
            args.batch_size,
        )

    except Exception as e:
        logger.error(f"Error in MongoDB export: {e}")
        raise
    finally:
        if "mongo_manager" in locals():
            mongo_manager.close()


if __name__ == "__main__":
    main()