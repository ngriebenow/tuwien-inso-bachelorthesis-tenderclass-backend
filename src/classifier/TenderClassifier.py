from typing import List
from simpletransformers.classification import ClassificationModel


class TenderClassifier:

    def __init__(self):
        self.model = ClassificationModel('bert', 'outputs/')

    def filter(self, tenders):

        titles = list(map(lambda x: x.get_title("DE"), tenders))
        predictions = self.model.predict(titles)
        tuples = zip(titles, predictions)

        selected_tenders = [t for t,p in tuples if p == 1]
        return selected_tenders
