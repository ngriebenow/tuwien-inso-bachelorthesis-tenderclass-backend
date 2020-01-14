from fetcher.ted.TedFetcher import TedFetcher
from entity.Tender import Tender

class TenderDownloader:

    def __init__(self):
        self.ted_fetcher = TedFetcher()

    def get(self, count : int, load_documents = False : bool, search_criteria = "" : str, languages = ["DE"] : List[str], page_offset = 0 : int) -> List[Tender]:
        return self.ted_fetcher.get(count, load_documents, search_criteria, languages, page_offset)