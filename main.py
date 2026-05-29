from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from textblob import TextBlob
import spacy

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return redirect(url_for("add", **request.args))


@app.route("/add")
def add():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    if a is None or b is None:
        return jsonify({"error": "Query parameters 'a' and 'b' are required"}), 400
    return jsonify({"result": a + b})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "JSON body with field 'text' is required"}), 400

    text = data["text"]

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        sentiment = "Positiv"
    elif polarity < 0:
        sentiment = "Negativ"
    else:
        sentiment = "Neutral"

    doc = nlp(text)
    keywords = list({token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN", "VERB") and not token.is_stop})

    return jsonify({"sentiment": sentiment, "polarity": round(polarity, 4), "keywords": keywords})


if __name__ == "__main__":
    app.run(port=8000)
