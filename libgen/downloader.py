import os
import requests
import time
from concurrent import futures
from tqdm import tqdm

from core.manage import settings


class Downloader:
    def _download_file(self, book):
        if book is not None:
            try:
                response = requests.get(
                    book.links["IPFS.io"],
                    headers=settings.get("download_file_headers"),
                    stream=True,
                )

                if response.status_code == 200:
                    os.makedirs(settings.get("DOWNLOAD_PATH", "./books"), exist_ok=True)
                    file_size = int(response.headers.get("content-length", 0))

                    path = f"./books/{book.title}.{book.extension}"
                    with open(path, "wb") as file, tqdm(
                        desc="Downloading",
                        total=file_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar:
                        for data in response.iter_content(chunk_size=1024):
                            file.write(data)
                            bar.update(len(data))

                    print("File downloaded successfully")
                else:
                    print("Error: Unable to download file")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def process_links(self, books: list):
        with futures.ProcessPoolExecutor() as executor:
            results = []
            for book in books:
                future = executor.submit(self._download_file, book)
                # time.sleep(settings.get("PROCESS_DELAY", 1))
                results.append(future)

            links = []
            for r in futures.as_completed(results):
                result = r.result()
                links.append(result)

            return links
