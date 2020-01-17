from typing import List
from simpletransformers.classification import ClassificationModel
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

args = {
    'learning_rate': 1e-4,
    'overwrite_output_dir': True
}


class TenderModel:
    """
    This class provides the Machine Learning model and classifies tenders based on previous training data.
    """

    def __init__(self):
        try:
            self.model = ClassificationModel('bert', './outputs/', use_cuda=False, args=args)
        except Exception as ex:
            logger.error(f"could not load model from /outputs due to {str(ex)}, creating new model")
            self.create_new_model()

    def __convert_to_input(self, tenders):
        titles = list(map(lambda x: x.get_title("DE"), tenders))
        return titles

    def classify(self, tenders):
        titles = self.__convert_to_input(tenders)
        predictions, raw_output = self.model.predict(titles)
        tuples = zip(tenders, predictions)

        selected_tenders = [t for t,p in tuples if p == 1]
        return selected_tenders

    def train(self, labelled_tenders):

        tenders = [i for i, j in labelled_tenders]
        labels = [j for i, j in labelled_tenders]

        titles = self.__convert_to_input(tenders)
        data_input = pd.DataFrame(zip(titles, labels))
        self.model.train_model(data_input)

    def create_new_model(self):
        self.model = ClassificationModel('bert', 'bert-base-german-cased', use_cuda=False, args=args)
