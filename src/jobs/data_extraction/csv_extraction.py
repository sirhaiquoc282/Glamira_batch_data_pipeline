from utils.gcs_utils import GCSManager
from utils.logger import Logger
from pathlib import Path


def extract_csv_to_gcs(logger, gcs_manager, bucket_name, base_path, file_path):
    try:
        target_path = f"{bucket_name}/{base_path}/{Path(file_path).name}"
        with open(file_path, "rb") as local_file:
            with gcs_manager._fs.open(target_path, "wb") as gcs_file:
                gcs_file.write(local_file.read())
        logger.info(f"Successfully uploaded {file_path} to GCS at {target_path}")
    except Exception as e:
        logger.error(f"Failed to upload {file_path} to GCS: {e}")
        return False


if __name__ == "__main__":

    logger = Logger(name="csv_to_gcs")
    gcs_manager = GCSManager()
    bucket_name = "my_bucket"
    base_path = "my_base_path"
    file_path = "my_file_path"
    extract_csv_to_gcs(logger, gcs_manager, bucket_name, base_path, file_path)
