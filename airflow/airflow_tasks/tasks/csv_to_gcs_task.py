import argparse
import logging
from pathlib import Path

from utils.gcs_utils import GCSManager
from utils.logger import Logger
from configs.settings import (
    FLATFILE_PATHS,
    LOG_FILE,
    LOG_LEVEL,
    LOG_NAME,
    BUCKET_NAME,
    CREDENTIAL_PATH,
    BASE_PATH,
    log_levels,
)


def upload_csv_files(logger, gcs_manager, bucket_name, file_paths, base_path):
    for file_path in file_paths:
        try:
            target_path = f"{bucket_name}/{base_path}/csv_files/{Path(file_path).name}"
            with open(file_path, "rb") as local_file:
                with gcs_manager._fs.open(target_path, "wb") as gcs_file:
                    gcs_file.write(local_file.read())
            logger.info(f"Uploaded CSV file {file_path} successfully")
        except Exception as e:
            logger.error(f"Failure to upload CSV file {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="CSV to GCS Upload")
    parser.add_argument(
        "--csv_file_paths",
        type=str,
        nargs="+",
        default=FLATFILE_PATHS,
        help="Paths to local CSV files for upload",
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
        gcs_manager = GCSManager(logger, args.credential_path)

        upload_csv_files(
            logger,
            gcs_manager,
            args.bucket_name,
            args.csv_file_paths,
            args.base_path,
        )

    except Exception as e:
        logger.error(f"Error in CSV upload: {e}")
        raise


if __name__ == "__main__":
    main()
