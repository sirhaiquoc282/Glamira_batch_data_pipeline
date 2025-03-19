from google.cloud import storage
from gcsfs import GCSFileSystem
import json
from pathlib import Path


class GCSManager:
    def __init__(self, logger, credential_path=None):
        self._fs = GCSFileSystem(token=credential_path)
        self.logger = logger
        self._client = (
            storage.Client.from_service_account_json(credential_path)
            if credential_path
            else storage.Client()
        )

    def load_checkpoint(self, bucket_name, checkpoint_path):
        full_path = f"{bucket_name}/{checkpoint_path}"
        try:
            if self._fs.exists(full_path):
                with self._fs.open(full_path, "r") as f:
                    data = json.load(f)
                    return data.get("last_id"), int(data.get("last_part", 0))
            return None, 0
        except Exception as e:
            self.logger.warning(f"Load checkpoint error: {e}")
            return None, 0

    def save_checkpoint(self, bucket_name, checkpoint_path, last_id, part_number):
        full_path = f"{bucket_name}/{checkpoint_path}"
        try:
            checkpoint_dir = Path(checkpoint_path).parent
            self._fs.makedirs(f"{bucket_name}/{checkpoint_dir}", exist_ok=True)

            with self._fs.open(full_path, "w") as f:
                json.dump({"last_id": str(last_id), "last_part": part_number}, f)
        except Exception as e:
            self.logger.error(f"Save checkpoint error: {e}")
            raise

    def upload_batch(self, bucket_name, target_path, records, part_number):
        try:
            target_path = f"{bucket_name}/{target_path}_part-{part_number:04d}.jsonl"
            with self._fs.open(target_path, "wb") as f:
                f.write("\n".join(records).encode("utf-8"))
            self.logger.info(f"Uploaded {len(records)} records to {target_path}")
            return True
        except Exception as e:
            self.logger.error(f"Upload error: {e}")
            return False
            
    def upload_file(self, bucket_name, source_path, target_path):
        try:
            full_target_path = f"{bucket_name}/{target_path}"
            with open(source_path, "rb") as local_file:
                with self._fs.open(full_target_path, "wb") as gcs_file:
                    gcs_file.write(local_file.read())
            self.logger.info(f"Uploaded file {source_path} to {full_target_path} successfully")
            return True
        except Exception as e:
            self.logger.error(f"Upload file error: {e}")
            return False