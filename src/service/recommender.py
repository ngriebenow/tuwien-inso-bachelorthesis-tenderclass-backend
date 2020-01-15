from src.classifier.TenderClassifier import TenderClassifier
from src.fetcher.TenderFetcher import TenderFetcher
from datetime import datetime


class Recommender:

    def __init__(self):
        self.tender_fetcher = TenderFetcher()
        self.tender_classifier = TenderClassifier()

    def get_recommendations(self, date):
        # TODO add date, count
        tenders = self.tender_fetcher.get(0, search_criteria=" AND PD=[" + datetime.strftime(date, "%Y%m%d") + "]")
        selected_tenders = self.tender_classifier.filter(tenders)
        return selected_tenders

