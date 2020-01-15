from typing import List
from simpletransformers.classification import ClassificationModel
import numpy as np
import pandas as pd


args = {
    'train_batch_size': 8,
    'eval_batch_size': 8,

    'gradient_accumulation_steps': 1,
    'num_train_epochs': 1,
    'weight_decay': 0,
    'learning_rate': 4e-2,
    'adam_epsilon': 1e-8,
    'warmup_steps': 0,
    'max_grad_norm': 1.0,

    'logging_steps': 50,
    'evaluate_during_training': False,
    'save_steps': 2000,
    'eval_all_checkpoints': False,

    'overwrite_output_dir': True,
    'reprocess_input_data': True,
}


class TenderModel:

    def __init__(self):
        self.model = ClassificationModel('bert', './outputs/', use_cuda=False, args=args)

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
        self.model = ClassificationModel('bert', 'bert-base-german-cased', use_cuda=False, args=args)
