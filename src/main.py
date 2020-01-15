from flask import Flask, request, jsonify
from src.service.TenderRecommender import TenderRecommender
from datetime import date
from src.service.TenderTrainer import TenderTrainer

app = Flask(__name__)

tender_recommender = TenderRecommender()
tender_trainer = TenderTrainer()


@app.route("/api/v1/model/recommendations", methods=['GET'])
def get_recommendations():
    today = date.today()
    tenders = tender_recommender.get_recommendations(today)
    return jsonify(list(map(lambda x: x.get_json(), tenders)))


@app.route("/api/v1/model/train", methods=['POST'])
def post_train_tenders():
    body = request.json
    train_tender_ids = body["ids"]
    train_tender_labels = body["labels"]
    tender_trainer.train(train_tender_ids, train_tender_labels)

    return "ok"


@app.route("/api/v1/model/new", methods=['POST'])
def post_create_new():
    body = request.json
    pos_number = body["pos_number"]
    neg_number = body["neg_number"]
    pos_search_criteria = body["pos_search_criteria"]
    neg_search_criteria = body["neg_search_criteria"]

    tender_trainer.create_and_init(pos_number,pos_search_criteria, neg_number, neg_search_criteria)

    return "ok"


if __name__ == "__main__":
    app.run()
