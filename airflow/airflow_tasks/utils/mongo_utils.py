from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError, BulkWriteError
from bson import ObjectId


class MongoManager:
    def __init__(self, logger, connection_uri, database_name=None, collection_name=None):
        self._client = MongoClient(connection_uri)
        self.logger = logger
        self.database_name = database_name
        self.collection_name = collection_name
        self._verify_connection()

    def _verify_connection(self):
        try:
            self._client.admin.command("ping")
            self.logger.info("Connected to MongoDB successfully")
        except PyMongoError as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_collection_cursor(self, db_name, collection_name, last_id=None):
        try:
            collection = self._client[db_name][collection_name]
            query = {"_id": {"$gt": ObjectId(last_id)}} if last_id else {}
            return collection.find(query).sort("_id", ASCENDING).batch_size(1000)
        except PyMongoError as e:
            self.logger.error(f"Failed to query data: {e}")
            raise

    def get_unique_ips(self):
        try:
            pipeline = [
                {"$group": {"_id": "$ip"}},
                {"$project": {"_id": 0, "ip": "$_id"}},
            ]
            cursor = self._client[self.database_name][self.collection_name].aggregate(
                pipeline, allowDiskUse=True
            )
            unique_ips = list(doc["ip"] for doc in cursor)
            self.logger.info(
                f"Got {len(unique_ips)} unique IPs from collection {self.collection_name} successfully."
            )
            return unique_ips
        except Exception as e:
            self.logger.error(
                f"Failed to get unique IPs from collection {self.collection_name}: {e}"
            )
            raise

    def insert_locations(self, locations_collection, locations_info):
        try:
            if not locations_info:
                self.logger.warning("Empty batch, skipping insert.")
                return

            self._client[self.database_name][locations_collection].insert_many(locations_info)
            self.logger.info(
                f"Inserted {len(locations_info)} locations into MongoDB successfully"
            )
            return True
        except BulkWriteError as e:
            self.logger.error(
                f"BulkWriteError - Failed to insert locations: {e.details}"
            )
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error when inserting locations: {e}")
            raise

    def get_checkpoint(self, checkpoint_collection, task_id):
        try:
            checkpoint = self._client[self.database_name][checkpoint_collection].find_one(
                {"task_id": task_id}
            )
            if checkpoint:
                return checkpoint
            return {"task_id": task_id, "last_processed_index": 0}
        except Exception as e:
            self.logger.error(f"Failed to get checkpoint: {e}")
            return {"task_id": task_id, "last_processed_index": 0}

    def update_checkpoint(self, checkpoint_collection, last_processed_index, task_id):
        try:
            self._client[self.database_name][checkpoint_collection].update_one(
                {"task_id": task_id},
                {"$set": {"last_processed_index": last_processed_index}},
                upsert=True
            )
            self.logger.info(f"Updated checkpoint to index {last_processed_index}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update checkpoint: {e}")
            return False

    def close(self):
        self._client.close()
        self.logger.info("MongoDB connection closed")