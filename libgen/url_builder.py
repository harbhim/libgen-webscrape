from pydantic import BaseModel, Field, PositiveInt

from core.manage import settings


class URLData(BaseModel):
    query: str
    field: str = Field(default="title")
    record_count: PositiveInt = Field(default=25)
    sort: str = Field(default="year")
    sortmode: str = Field(default="DESC")


class URLBehavior:
    def __init__(self, url_data: URLData):
        self.base_url = settings.get("BASE_URL")
        self.url_data = url_data

        if len(self.url_data.query) < 3:
            raise ValueError("The length of search query must be greater than 3")

    def get_url_unfiltered(self):
        query = self.url_data.query.replace(" ", "%20")
        url = f"{self.base_url}/search.php?req={query}&res={self.url_data.record_count}&column={self.url_data.field}"
        return url

    def get_url_filtered(self):
        url = self.get_url_unfiltered()
        url = f"{url}&sort={self.url_data.sort}&sortmode={self.url_data.sortmode}"
        return url
