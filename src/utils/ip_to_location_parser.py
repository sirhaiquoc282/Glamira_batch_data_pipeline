from IP2Location import IP2Location
from airflow_tasks.configs.settings import IP2LOCATION_FILE


class IPtoLocationParser:
    def __init__(self, logger, ip2location_file=IP2LOCATION_FILE):
        self.ip2location = IP2Location()
        self.ip2location.open(ip2location_file)
        self.logger = logger

    def get_location(self, ip):
        try:
            location_info = self.ip2location.get_all(ip)
            return {
                "ip": ip,
                "country_short": location_info.country_short,
                "country_long": location_info.country_long,
                "region": location_info.region,
                "city": location_info.city,
            }
        except Exception as e:
            self.logger.error(f"Failed to convert IP {ip} to location: {e}")
            return self._default_location(ip)

    def _default_location(self, ip):
        return {
            "ip": ip,
            "country_short": "Unknown",
            "country_long": "Unknown",
            "region": "Unknown",
            "city": "Unknown",
        }
