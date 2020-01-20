import datetime
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('src')])

from src.classifier.SimpleTenderModel import SimpleTenderModel
from src.classifier.TransformerTenderModel import TransformerTenderModel
from src.persistence.TenderPersistence import TenderPersistence

from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from src.service.TenderRecommender import TenderRecommender
from src.service.TenderTrainer import TenderTrainer
from datetime import date
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
logger.info("start tenderclass-backend")

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'tenderclass-backend': "API specification for the Machine Learning classification solution for public tenders"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

tender_model = TransformerTenderModel()
tender_recommender = TenderRecommender(tender_model)
tender_trainer = TenderTrainer(tender_model)
tender_persistence = TenderPersistence()


@app.route("/api/v1/persistence/save", methods=['POST'])
def post_save():
    path = request.json["path"]
    search_criteria = request.json["search_criteria"]
    count = int(request.args.get('count'))
    tenders = tender_recommender.get_all(count, search_criteria=search_criteria)
    tender_persistence.save(tenders, path)

    return "ok"


@app.route("/api/v1/persistence/train", methods=['POST'])
def post_train_from_persistence():
    neg_path = request.json["neg_path"]
    pos_path = request.json["pos_path"]
    neg_tenders = tender_persistence.load(neg_path)
    pos_tenders = tender_persistence.load(pos_path)
    tender_trainer.train_from_entities(neg_tenders, pos_tenders)

    return "ok"


@app.route("/api/v1/web", methods=['GET'])
def get_all():
    count = int(request.args.get('count'))
    date_filter = request.args.get('date')
    search_criteria = ""
    if date_filter:
        search_criteria = " AND PD=[" + date_filter + "]"
    tenders = tender_recommender.get_all(count, search_criteria=search_criteria)
    return jsonify(list(map(lambda x: x.get_dict(), tenders)))


@app.route("/api/v1/web/recommendations", methods=['GET'])
def get_recommendations():
    count = int(request.args.get('count'))
    today = request.args.get('date')
    if today is None:
        today = datetime.strftime(date.today(), "%Y%m%d")
    search_criteria = " AND PD=[" + today + "]"
    tenders = tender_recommender.get_recommendations(count, search_criteria)
    return jsonify(list(map(lambda x: x.get_dict(), tenders)))


@app.route("/api/v1/web/train", methods=['POST'])
def post_train_from_web():
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

    tender_trainer.create_and_init(pos_number, pos_search_criteria, neg_number, neg_search_criteria)

    return "ok"


if __name__ == "__main__":
    app.run()
