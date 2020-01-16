from src.classifier.TenderModel import TenderModel
from src.fetcher.TenderFetcher import TenderFetcher
import random


class TenderTrainer:
    """
    This class cooordinates training and creation of the machine learning model as well as preparation of data.
    """

    def __init__(self):
        self.tender_fetcher = TenderFetcher()
        self.tender_model = TenderModel()

    def train(self, tender_ids, labels):
        search_arg = " OR ".join(tender_ids)
        search_criteria = f" AND ND=[{search_arg}]"
        tenders = self.tender_fetcher.get(0, search_criteria=search_criteria)

        labelled_tenders = list(map(lambda x: (x, labels[tender_ids.index(x.id)], tenders)))

        self.tender_model.train(labelled_tenders)

    def create_and_init(self, pos_number, pos_search_criteria, neg_number, neg_search_criteria):
        pos_tenders = self.tender_fetcher.get(pos_number, search_criteria=pos_search_criteria)
        neg_tenders = self.tender_fetcher.get(neg_number, search_criteria=neg_search_criteria)

        pos_labels = [1]*len(pos_tenders)
        neg_labels = [0]*len(neg_tenders)

        labelled_tenders = list(zip(pos_tenders, pos_labels)) + list(zip(neg_tenders, neg_labels))

        random.shuffle(labelled_tenders)

        self.tender_model.create_new_model()
        self.tender_model.train(labelled_tenders)


