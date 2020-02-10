from src.classifier.TransformerModel import TransformerModel
from src.fetcher.Fetcher import Fetcher
from datetime import datetime


class Recommender:
    """
    This class gets all tenders from today, classifies them and returns only the positive tenders.
    """

    def __init__(self, tender_model):
        self.tender_fetcher = Fetcher()
        self.tender_model = tender_model
        self.cached_selected_tenders = []
        self.cached_search_criteria = ""

    def get_recommendations(self, count, search_criteria = ""):
        if not self.cached_selected_tenders or self.cached_selected_tenders != search_criteria:
            tenders = self.tender_fetcher.get(count, search_criteria=search_criteria)
            self.cached_selected_tenders = self.tender_model.classify(tenders)
        return self.cached_selected_tenders

    def get_all(self, count, search_criteria=""):
        tenders = self.tender_fetcher.get(count, search_criteria=search_criteria)
        return tenders

