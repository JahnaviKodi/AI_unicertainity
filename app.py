from flask import Flask, request, jsonify, render_template
from src.pipeline import Pipeline

app = Flask(__name__)
pipeline = Pipeline()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    result = pipeline.run(query)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True) 
