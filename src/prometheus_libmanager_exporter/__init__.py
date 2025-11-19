from typing import Iterable

import prometheus_client
import structlog
from prometheus_client import Metric
from prometheus_client.core import GaugeMetricFamily

from .libmanager import Scraper


class Collector(prometheus_client.registry.Collector):
    def __init__(self, scraper: Scraper):
        self.__scraper = scraper

    def collect(self) -> Iterable[Metric]:
        status = GaugeMetricFamily("libmanager_entity_status", "Status of the libmanager entity", labels=["branch", "machine", "ip"])

        try:
            for entity in self.__scraper.scrape():
                status.add_metric([entity.branch, entity.machine, entity.ip], 1 if entity.online else 0)

        except Exception as e:
            structlog.get_logger().warning("Failed to scrape libmanager", exc_info=e)

        return [status]
