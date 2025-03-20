from IP2Location import IP2Location
from utils.logger import Logger
from utils.mongo_utils import MongoManager
from utils.ip_to_location_parser import IPtoLocationParser


def convert_ips_to_locations(
    logger, mongo_manager, ip_to_location_parser, db_name, collection_name, batch_size
):
    try:
        uniq_ips = mongo_manager.get_unique_ips()
        batch = []
        for ip in uniq_ips:
            location_info = ip_to_location_parser.get_location(ip)
            batch.append(location_info)
            if len(batch) >= batch_size:
                mongo_manager.insert_locations(collection_name, batch)
                logger.info(
                    f"Inserted {len(batch)} locations into {db_name}.{collection_name}"
                )
                batch = []
        if batch:
            mongo_manager.insert_locations(collection_name, batch)
            logger.info(
                f"Inserted {len(batch)} locations into {db_name}.{collection_name}"
            )
            batch = []
    except Exception as e:
        logger.error(f"Failed to convert IPs to locations: {e}")
        return False


if __name__ == "__main__":
    db_name = "my_db"
    collection_name = "my_collection"
    logger = Logger(name="ip_to_location")
    mongo_manager = MongoManager()
    ip_to_location_parser = IPtoLocationParser(logger=logger, ip2location=IP2Location())
    convert_ips_to_locations(
        logger,
        mongo_manager,
        ip_to_location_parser,
        db_name,
        collection_name,
        batch_size=100,
    )
