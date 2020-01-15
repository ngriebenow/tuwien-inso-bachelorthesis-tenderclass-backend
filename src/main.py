from flask import Flask
from src.fetcher.TenderFetcher import TenderFetcher
from src.service.TenderRecommender import TenderRecommender
from datetime import date
app = Flask(__name__)


@app.route("/api/v1/recommendation", methods=['GET'])
def get_recommendations():
    return "Hello World!"


if __name__ == "__main__":
    tr = TenderRecommender()
    today = date.today()
    tenders = tr.get_recommendations(today)

    s = list(map(lambda x: x.get_json(), tenders))
    print(s)

    #tf = TenderFetcher()
    #t = tf.get(1)
    #print(t[0].get_title("DE"))
    # app.run()
