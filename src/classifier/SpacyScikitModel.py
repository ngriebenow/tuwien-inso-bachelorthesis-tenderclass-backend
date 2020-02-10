import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import spacy
import string
import logging
import numpy as np

logger = logging.getLogger(__name__)

LANGUAGE = "DE"
MODEL_NAME = "scikit_model"
punctuations = string.punctuation


class SpacyScikitModel:

    def __init__(self):
        if LANGUAGE == "DE":
            from spacy.lang.de.stop_words import STOP_WORDS
            self.nlp = spacy.load('de_core_news_sm')
            self.domain_stopwords = ["Ausschreibung", "Bekanntmachung"]
            from spacy.lang.de import German
            self.parser = German()
        elif LANGUAGE == "EN":
            from spacy.lang.en.stop_words import STOP_WORDS
            self.nlp = spacy.load('en')
            self.domain_stopwords = ["contract", "system", "service", "tender", "company", "notice", "procurement",
                                     "work", "include", "support", "approximately", "management", "agreement",
                                     "office", "solution", "manage", "product", "design", "program", "project",
                                     "supply", "trust", "equipment"]
            from spacy.lang.en import English
            self.parser = English()
        else:
            raise Exception("unknown language")

        self.stopwords = list(STOP_WORDS)
        self.stopwords.extend(self.domain_stopwords)
        self.pipe = None

    def spacy_tokenizer(self, sentence):
        sentence_tokens = self.parser(sentence)
        sentence_tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in sentence_tokens]
        sentence_tokens = [word for word in sentence_tokens if word not in self.stopwords and word not in punctuations]
        return sentence_tokens

    class Predictors(TransformerMixin):

        def __clean_text(self, text):
            if text is None:
                return ""
            return str(text).strip().lower()

        def transform(self, X, **transform_params):
            return [self.__clean_text(text) for text in X]

        def fit(self, X, y=None, **fit_params):
            return self

        def get_params(self, deep=True):
            return {}

    def __load_model(self):
        if not self.pipe:
            self.pipe = joblib.load(MODEL_NAME)

    def __convert_to_input(self, tenders):
        titles = list(map(lambda x: x.get_title("DE"), tenders))
        return titles

    def classify(self, tenders):
        self.__load_model()

        titles = self.__convert_to_input(tenders)
        predictions = self.pipe.predict(titles)
        tuples = zip(tenders, predictions)
        selected_tenders = [t for t, p in tuples if p == 1]
        return selected_tenders

    def train(self, labelled_tenders):
        self.__load_model()

        tenders = [i for i, j in labelled_tenders]
        labels = [j for i, j in labelled_tenders]
        titles = self.__convert_to_input(tenders)

        training_df = pd.DataFrame({"title": titles, "label": labels})
        T = training_df["title"]
        y = training_df["label"]

        T_train, T_test, y_train, y_test = train_test_split(T, y, test_size=0.1, random_state=42)
        logger.info("start training")
        self.pipe.fit(T_train, y_train)
        logger.info("start testing")
        y_pred = self.pipe.predict(T_test)
        logger.info(f"accuracy: {self.pipe.score(T_test, y_test)} , tested with {len(T_test)} instances")
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        logger.info(f"tn: {tn} fp: {fp}")
        logger.info(f"fn: {fn} tp:{tp}")
        joblib.dump(self.pipe, MODEL_NAME)

    def create_new_model(self):
        vectorizer = CountVectorizer(tokenizer=self.spacy_tokenizer, ngram_range=(1, 2))

        classifier = LinearSVC()
        predictor = self.Predictors()

        self.pipe = Pipeline([("cleaner", predictor),
                              ('vectorizer', vectorizer),
                              ('classifier', classifier)])

        joblib.dump(self.pipe, MODEL_NAME)
