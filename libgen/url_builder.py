from manager.manage import settings


class URLBuilder:
    def __init__(self, query: str, field: str="title"):
        self.base_url: str = settings.get("BASE_URL","")
        self.query = "%20".join(query.split(" "))
        self.field = field

        if len(self.query) < 3:
            raise ValueError("The length of search query must be grater than 3")

    def get_url_unfiltered(self):
        return f"{self.base_url}/search.php?req={self.query}&column={self.field}"

    def get_url_filtered(self, field: str="year", mode: str="DESC"):
        url = self.get_url_unfiltered()
        url = f"{url}&sort={field}&sortmode={mode}"
        return url

        
