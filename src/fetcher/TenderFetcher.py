from typing import List
from fetcher.ted.TedFetcher import TedFetcher
from entity.Tender import Tender

class TenderFetcher:

    def __init__(self):
        self.ted_fetcher = TedFetcher()

    def get(self, count : int, load_documents : bool = False, search_criteria : str = "", languages : List[str] = ["DE"], page_offset : int = 0) -> List[Tender]:
        return self.ted_fetcher.get(count, load_documents, search_criteria, languages, page_offset)


if __name__ == "__main__":
    tender_fetcher = TenderFetcher()
    tender_fetcher.get(1)