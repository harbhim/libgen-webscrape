import argparse
from libgen.link_parser import DownloadLinks

from libgen.url_builder import URLData, URLBehavior
from libgen.search_request import SearchRequest
from libgen.downloader import Downloader

parser = argparse.ArgumentParser()
parser.add_argument("-title", "--title", help="Title")
parser.add_argument("-isbn", "--isbn", help="ISBN")
parser.add_argument("-author", "--author", help="Author")
args = parser.parse_args()


def get_kwargs(args):
    if args.isbn is not None:
        return {"query": str(args.isbn), "field": "identifier"}
    elif args.author is not None:
        return {"query": str(args.author), "field": "author"}
    elif args.title is not None:
        return {"query": str(args.title)}
    else:
        return None


kwargs = get_kwargs(args)
print(kwargs)

if kwargs is not None:
    url_data = URLData(**kwargs)
    url = URLBehavior(url_data).get_url_filtered()
    records = SearchRequest(url).aggregate_request_data()
    links = DownloadLinks(records).resolve_download_links()
    results = Downloader().process_links(links)
    print(results)
