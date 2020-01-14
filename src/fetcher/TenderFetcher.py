from typing import List

from src.entity import Tender
from src.fetcher.ted.TedFetcher import TedFetcher


class TenderFetcher:

    def __init__(self):
        self.ted_fetcher = TedFetcher()

    def get(self, count: int, load_documents: bool = False, search_criteria: str = "", languages: List[str] = ["DE"], page_offset: int = 0) -> List[Tender]:
        return self.ted_fetcher.get(count, load_documents, search_criteria, languages, page_offset)

