import argparse
from libgen.link_parser import DownloadLinks

from libgen.url_builder import URLData, URLBehavior
from libgen.search_request import SearchRequest
from libgen.downloader import Downloader

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", help="Search Query")
args = parser.parse_args()

if args.query and (query := args.query):
    url_data = URLData(query=query)
    url = URLBehavior(url_data).get_url_filtered()
    records = SearchRequest(url).aggregate_request_data()
    links = DownloadLinks(records).resolve_download_links()
    results = Downloader().process_links(links)
    print(results)
