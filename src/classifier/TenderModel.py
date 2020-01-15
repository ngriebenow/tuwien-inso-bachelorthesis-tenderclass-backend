from typing import List
from simpletransformers.classification import ClassificationModel
import numpy as np
import pandas as pd


class TenderModel:

    def __init__(self):
        self.model = ClassificationModel('bert', './outputs/', use_cuda=False)

    def convert_to_input(self, tenders):
        titles = list(map(lambda x: x.get_title("DE"), tenders))
        return titles

    def classify(self, tenders):
        titles = self.convert_to_input(tenders)
        predictions, raw_output = self.model.predict(titles)
        # predictions = np.array([1]*len(titles))
        tuples = zip(tenders, predictions)

        selected_tenders = [t for t,p in tuples if p == 1]
        return selected_tenders

    def train(self, labelled_tenders):

        tenders = [i for i, j in labelled_tenders]
        labels = [j for i, j in labelled_tenders]

        titles = self.convert_to_input(tenders)
        data_input = pd.DataFrame(zip(titles, labels))
        self.model.train_model(data_input)

    def create_new_model(self):
        self.model = ClassificationModel('bert', 'bert-base-german-cased', use_cuda=False, args={'overwrite_output_dir': True})
