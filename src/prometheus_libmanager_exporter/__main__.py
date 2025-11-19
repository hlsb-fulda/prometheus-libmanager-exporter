import os
import time
from typing import Callable

import click
from prometheus_client import REGISTRY, start_http_server

from . import Scraper, Collector


def load_credential(key: str, default: str = None) -> Callable[[], str | None]:
    def load() -> str | None:
        base = os.environ.get("CREDENTIALS_DIRECTORY")
        if base is None:
            return default

        path = os.path.join(base, key)

        if not os.path.exists(path):
            return default

        with open(path, encoding="utf-8") as f:
            return f.read().removesuffix("\n")

    return load


@click.command()
@click.argument("url", default="https://localhost/libmanager")
@click.option("--insecure", default=False, is_flag=True, help="Allow insecure connection to the libmanager")
@click.option("--username", default=load_credential("username", "admin"), help="Username to login with")
@click.option("--password", default=load_credential("password"), help="Password to login with")
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
