from typing import List
from simpletransformers.classification import ClassificationModel
import numpy as np


class TenderClassifier:

    def __init__(self):
        pass
        # self.model = ClassificationModel('bert', './outputs/', use_cuda=False)

    def filter(self, tenders):

        titles = list(map(lambda x: x.get_title("DE"), tenders))
        # predictions, raw_output = self.model.predict(titles)
        predictions = np.array([1]*len(titles))
        tuples = zip(tenders, predictions)

        selected_tenders = [t for t,p in tuples if p == 1]
        return selected_tenders
