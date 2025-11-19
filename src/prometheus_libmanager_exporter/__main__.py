import time

import click
from prometheus_client import REGISTRY, start_http_server

from . import Scraper, Collector


@click.command()
@click.argument("url", default="https://localhost/libmanager")
@click.option("--insecure", default=False, is_flag=True, help="Allow insecure connection to the libmanager")
@click.option("--username", envvar="LIBMANAGER_USERNAME", default="admin", help="Username to login with")
@click.option("--password", envvar="LIBMANAGER_PASSWORD", default="", help="Password to login with")
@click.option("--port", default=10386, type=int, help="Port to listen on")
def main(url, insecure, username, password, port):
    scraper = Scraper(url, username, password, insecure)

    collector = Collector(scraper)
    REGISTRY.register(collector)

    start_http_server(port)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
