from typing import List
from src.fetcher.ted.TedFetcher import TedFetcher


class Fetcher:
    """
    This class fetches tenders from provides databases.
    Currently, only TED serves as database.
    """

    def __init__(self):
        self.ted_fetcher = TedFetcher()

    def get(self, count: int, load_documents: bool = False, search_criteria: str = "", languages: List[str] = ["DE"], page_offset: int = 0):
        return self.ted_fetcher.get(count, load_documents, search_criteria, languages, page_offset)

