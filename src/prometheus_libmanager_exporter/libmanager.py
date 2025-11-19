from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin

import requests
import structlog
from bs4 import BeautifulSoup
from prometheus_client import Summary, Counter, Histogram

metric_scrape_duration = Histogram("libmanager_scrape_duration_seconds", "Duration of the libmanager scrape")
metric_scrape_failures = Counter("libmanager_scrape_failures_total", "Number of libmanager scrape failures")
metric_scrape_request_duration = Summary(
    "libmanager_scrape_request_duration_seconds", "Duration of the libmanager scrape request", ["request"]
)


@dataclass
class Entity:
    branch: str
    machine: str

    online: bool

    ip: str


class Scraper(object):
    def __init__(self, url, username, password, insecure=False):
        self.__url = url
        self.__username = username
        self.__password = password

        self.__session = requests.Session()
        self.__session.verify = not insecure

    @metric_scrape_duration.time()
    @metric_scrape_failures.count_exceptions()
    def scrape(self):
        log = structlog.get_logger(run=datetime.now().isoformat())
        log.info("Scraping", url=self.__url)

        # Get the login page to get the CSRF token
        with metric_scrape_request_duration.labels("init").time():
            response = self.__session.get(urljoin(self.__url, "users/login"))
        response.raise_for_status()

        log.debug("Got login page", status=response.status_code)

        # Extract the CSRF token from the form
        response = BeautifulSoup(response.text, "html.parser")
        request_verification_token = response.find("input", attrs={"name": "__RequestVerificationToken"})["value"]

        # Submit the login form
        # We need a redirect while logging in to distinguish between failed and successful logins
        with metric_scrape_request_duration.labels("login").time():
            response = self.__session.post(
                urljoin(self.__url, "users/login"),
                data={
                    "Username": self.__username,
                    "Password": self.__password,
                    "RememberMe": True,
                    "__RequestVerificationToken": request_verification_token,
                    "signin": "true",
                    "language": "EN",
                },
                params={"ReturnUrl": "libmanager"},
                allow_redirects=False,
            )

        log.debug("Logged in", status=response.status_code)

        if response.status_code != 302:
            # Getting an OK response means we are *not* logged in
            raise Exception("Failed to login")

        # Query the dashboard
        with metric_scrape_request_duration.labels("query").time():
            response = self.__session.post(urljoin(self.__url, "dashboard/health"), data={"type": "0"})
        response.raise_for_status()

        log.debug("Dashboard fetched", status=response.status_code)

        # Parse the dashboard for the status values
        response = BeautifulSoup(response.text, "html.parser")
        for entry in response.find_all("a", attrs={"class": ["station"], "data-branch": True, "data-machine": True}):
            yield Entity(
                branch=entry.attrs["data-branch"],
                machine=entry.attrs["data-machine"],
                online="list-group-item-success" in entry.attrs["class"],
                ip=entry.attrs["data-ip"],
            )

        log.debug("Scrape finished")
