from flask import Flask
from src.fetcher.TenderFetcher import TenderFetcher

app = Flask(__name__)


@app.route("/api/v1/recommendation", methods=['GET'])
def get_recommendations():
    return "Hello World!"


if __name__ == "__main__":
    tf = TenderFetcher()
    t = tf.get(1)
    print(t[0].get_title("DE"))
    # app.run()
