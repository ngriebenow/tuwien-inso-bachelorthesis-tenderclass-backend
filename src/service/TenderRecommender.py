from src.classifier.TransformerTenderModel import TransformerTenderModel
from src.fetcher.TenderFetcher import TenderFetcher
from datetime import datetime


class TenderRecommender:
    """
    This class gets all tenders from today, classifies them and returns only the positive tenders.
    """

    def __init__(self):
        self.tender_fetcher = TenderFetcher()
        self.tender_model = TransformerTenderModel()
        self.cached_selected_tenders = []

    def get_recommendations(self, count, date):
        if not self.cached_selected_tenders:
            tenders = self.tender_fetcher.get(count, search_criteria=" AND PD=[" + datetime.strftime(date, "%Y%m%d") + "]")
            self.cached_selected_tenders = self.tender_model.classify(tenders)
        return self.cached_selected_tenders

    def get_all(self, count):
        tenders = self.tender_fetcher.get(count)
        return tenders

