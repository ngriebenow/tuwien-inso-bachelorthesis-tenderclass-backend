from typing import List
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import logging

from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

args = {
    'learning_rate': 1e-4,
    'overwrite_output_dir': True
}


class TransformerTenderModel:
    """
    This class provides the Machine Learning model and classifies tenders based on previous training data.
    """

    def load_model(self):
        if not self.model:
            from simpletransformers.classification import ClassificationModel
            try:
                self.model = ClassificationModel('bert', './outputs/', use_cuda=False, args=args)
            except Exception as ex:
                logger.error(f"could not load model from /outputs due to {str(ex)}, creating new model")
                self.create_new_model()

    def __init__(self):
        self.model = None

    def __convert_to_input(self, tenders):
        titles = list(map(lambda x: x.get_title("DE"), tenders))
        return titles

    def classify(self, tenders):
        self.load_model()

        titles = self.__convert_to_input(tenders)
        predictions, raw_output = self.model.predict(titles)
        tuples = zip(tenders, predictions)

        selected_tenders = [t for t,p in tuples if p == 1]
        return selected_tenders

    def train(self, labelled_tenders):
        self.load_model()

        tenders = [i for i, j in labelled_tenders]
        tenders = self.__convert_to_input(tenders)
        labels = [j for i, j in labelled_tenders]


        tenders_train, tenders_test, labels_train, labels_test = train_test_split(tenders, labels, test_size=0.1, random_state=42)

        data_input = pd.DataFrame(zip(tenders_train, labels_train))

        self.model.train_model(data_input)

        labels_pred, raw_output = self.model.predict(tenders_test)
        tn, fp, fn, tp = confusion_matrix(labels_test, labels_pred).ravel()
        logger.info(f"tn: {tn} fp: {fp}")
        logger.info(f"fn: {fn} tp:{tp}")



    def create_new_model(self):
        from simpletransformers.classification import ClassificationModel
        self.model = ClassificationModel('bert', 'bert-base-german-cased', use_cuda=False, args=args)
