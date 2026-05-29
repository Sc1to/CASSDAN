from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

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
    data = request.get_json(force=True, silent=True)
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

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    tagged = nltk.pos_tag(tokens)
    # Keep nouns (NN*) and verbs (VB*), filter stopwords
    keywords = list({word for word, tag in tagged
                     if tag.startswith(("NN", "VB")) and word.lower() not in stop_words and word.isalpha()})

    return jsonify({"sentiment": sentiment, "polarity": round(polarity, 4), "keywords": keywords})


if __name__ == "__main__":
    app.run(port=8000)
