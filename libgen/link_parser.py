import time
import requests
from concurrent import futures
from bs4 import BeautifulSoup

from core.manage import settings

MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io"]
EXTENSIONS = ["pdf", "epub"]
LANGUAGES = ["English", "english"]


class DownloadLinks:
    def __init__(self, items: list):
        self.items = items

    def _get_filtered_records(self):
        filtered_records = [
            record
            for record in self.items
            if record["Language"] in LANGUAGES and record["Extension"] in EXTENSIONS
        ]
        return filtered_records

    def _request_page(self, book: tuple):
        print("process_started")

        headers = settings.get("download_page_headers")
        max_retry = settings.get("MAX_RETRY", 3)
        retry_delay = settings.get("RETRY_DELAY", 3)

        for _ in range(max_retry):
            try:
                page = requests.get(book[2], headers=headers)
                page.raise_for_status()
                soup = BeautifulSoup(page.text, "html.parser")
                links = soup.find_all("a", string=MIRROR_SOURCES)
                download_links = {link.string: link["href"] for link in links}
                return {
                    "id": book[0],
                    "title": book[1],
                    "url": book[2],
                    "extension": book[3],
                    "links": download_links,
                }

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                time.sleep(retry_delay)

    def resolve_download_links(self):
        records = self._get_filtered_records()
        books = [
            (record["ID"], record["Title"], record["Mirror_1"], record["Extension"])
            for record in records
        ]

        with futures.ProcessPoolExecutor() as executor:
            results = []
            for book in books:
                future = executor.submit(self._request_page, book)
                time.sleep(settings.get("PROCESS_DELAY", 2))
                results.append(future)

            links = []
            for r in futures.as_completed(results):
                result = r.result()
                links.append(result)

            return links
