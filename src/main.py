from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/recommendations", methods=['GET'])
    def get_recommendations():
        return "Hello World!"

if __name__ == "__main__":
    app.run()