import os
import logging

# MongoDB settings
MONGO_URI = "mongodb://<user>:<password>@<internal_ip>:27017/?authSource=admin"
DATABASE_NAME = "countly"
COLLECTION_NAME = "summary"
LOCATIONS_COLLECTION = "locations"
CHECKPOINT_COLLECTION = "processing_checkpoints"

# GCS settings
BUCKET_NAME = "data-exports"
BASE_PATH = "data/exports"
CREDENTIAL_PATH = os.environ.get("GCP_CREDENTIAL_PATH", "/path/to/credentials.json")

# File paths
FLATFILE_PATHS = []  # Default empty list
IP2LOCATION_FILE = "data/IP-COUNTRY-REGION-CITY.BIN"

# Processing settings
BATCH_SIZE = 1000000
DB_COLLECTIONS = []  # Default empty list

# Logging settings
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "data_pipeline.log")
LOG_NAME = "data_pipeline"
LOG_LEVEL = "info"

# Mapping for log levels
log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
