from typing import List

from simpletransformers.classification import ClassificationModel

class TenderClassifier:

    def __init__(self):
        self.model = ClassificationModel('roberta', 'outputs/')

    def filter(self, tenders):

        titles = list(map(lambda x: x.get_title("DE"), tenders))
        predictions = self.model.predict(titles)

        cpvs = []
