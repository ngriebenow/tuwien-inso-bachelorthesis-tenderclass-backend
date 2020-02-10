# Use src path so that the python interpreter can access all modules
import datetime
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('src')])

# import all own modules
from src.classifier.SpacyScikitModel import SpacyScikitModel
from src.classifier.TransformerModel import TransformerModel
from src.persistence.Persistence import Persistence
from src.service.Recommender import Recommender
from src.service.Trainer import Trainer

# import dependencies
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from datetime import date
from datetime import datetime
import logging

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger.info("start tenderclass-backend")

app = Flask(__name__)
CORS(app)

# set up Swagger documentation
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

# TODO: select the Machine Learning model 
tender_model = SpacyScikitModel()
#tender_model = TransformerModel()

tender_recommender = Recommender(tender_model)
tender_trainer = Trainer(tender_model)
tender_persistence = Persistence()


@app.route("/api/v1/web/recommendations", methods=['GET'])
def get_recommendations():
    # use query parameters to overwrite default count and date
    count = int(request.args.get('count'))
    if count is None:
        # download all tenders (indicated by count=0)
        count = 0
    today = request.args.get('date')
    if today is None:
        # DEFAULT: get tenders of today
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



### Additional endpoints for saving tenders and training tenders from the file system.
### NOT documented yet because it is not scope of this bachelor thesis
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


if __name__ == "__main__":
    app.run()
