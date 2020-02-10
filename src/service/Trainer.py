from src.classifier.TransformerModel import TransformerModel
from src.fetcher.Fetcher import Fetcher
import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Trainer:
    """
    This class cooordinates training and creation of the machine learning model as well as preparation of data.
    """

    def __init__(self, tender_model):
        self.tender_fetcher = Fetcher()
        self.tender_model = tender_model

    def train(self, tender_ids, labels):
        search_arg = " OR ".join(tender_ids)
        search_criteria = f" AND ND=[{search_arg}]"
        tenders = self.tender_fetcher.get(0, search_criteria=search_criteria)

        labelled_tenders = list(map(lambda x: (x, labels[tender_ids.index(x.id)], tenders)))

        self.tender_model.train(labelled_tenders)

    def create_and_init(self, pos_number, pos_search_criteria, neg_number, neg_search_criteria):
        self.tender_model.create_new_model()
        if (pos_number + neg_number) == 0:
            return

        pos_tenders = self.tender_fetcher.get(pos_number, search_criteria=pos_search_criteria)
        neg_tenders = self.tender_fetcher.get(neg_number, search_criteria=neg_search_criteria)

        pos_labels = [1]*len(pos_tenders)
        neg_labels = [0]*len(neg_tenders)

        labelled_tenders = list(zip(pos_tenders, pos_labels)) + list(zip(neg_tenders, neg_labels))

        random.shuffle(labelled_tenders)

        self.tender_model.train(labelled_tenders)
        logger.info("tenders successfully downloaded and labelled")

    def train_from_entities(self, neg_tenders, pos_tenders):
        pos_labels = [1] * len(pos_tenders)
        neg_labels = [0] * len(neg_tenders)

        labelled_tenders = list(zip(pos_tenders, pos_labels)) + list(zip(neg_tenders, neg_labels))

        random.shuffle(labelled_tenders)

        self.tender_model.train(labelled_tenders)


