import time

import click
from prometheus_client import REGISTRY, start_http_server

from . import Scraper, Collector


@click.command()
@click.argument("url", default="https://localhost/libmanager")
@click.option("--insecure", default=False, is_flag=True, help="Allow insecure connection to the libmanager")
@click.option("--username", default="admin")
@click.option("--password", default="")
def main(url, insecure, username, password):
    scraper = Scraper(url, username, password, insecure)

    collector = Collector(scraper)
    REGISTRY.register(collector)

    start_http_server(10386)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
