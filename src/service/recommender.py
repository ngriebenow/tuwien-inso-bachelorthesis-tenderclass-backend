from src.classifier.TenderClassifier import TenderClassifier
from src.fetcher.TenderFetcher import TenderFetcher


class Recommender:

    def __init__(self):
        self.tender_fetcher = TenderFetcher()
        self.tender_classifier = TenderClassifier()

    def get_recommendations(self, date):
        # TODO add date, count
        tenders = self.tender_fetcher.get(10)
        self.tender_classifier.g

