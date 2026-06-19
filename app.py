from flask import Flask, request, jsonify, render_template
from src.pipeline import Pipeline
from src.database import db, QueryLog
from sqlalchemy import func
import time
import csv
import io
from flask import Response
import os

app = Flask(__name__)
pipeline = Pipeline()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///queries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs("uploads", exist_ok=True)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    start_time = time.time()
    result = pipeline.run(query)
    response_time = round(time.time() - start_time, 2)

    log = QueryLog(
        query=query,
        decision=result["decision"],
        confidence=result["confidence"],
        boundary=result["boundary"],
        response=result["response"],
        response_time=response_time
    )
    db.session.add(log)
    db.session.commit()

    result["response_time"] = response_time
    result["id"] = log.id
    return jsonify(result)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = file.filename

    if filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Read file content
    content = ""

    if filename.endswith(".txt"):
        content = file.read().decode("utf-8", errors="ignore")

    elif filename.endswith(".pdf"):
        try:
            import PyPDF2
            import io
            reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            for page in reader.pages:
                content += page.extract_text() or ""
        except Exception as e:
            return jsonify({"error": f"PDF reading failed: {str(e)}"}), 400

    elif filename.endswith(".docx"):
        try:
            import docx
            import io
            doc = docx.Document(io.BytesIO(file.read()))
            content = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            return jsonify({"error": f"DOCX reading failed: {str(e)}"}), 400

    else:
        return jsonify({"error": "Only .txt, .pdf, and .docx files are supported"}), 400

    # Truncate if too long
    content = content[:3000]

    return jsonify({
        "filename": filename,
        "content": content,
        "length": len(content)
    })

@app.route("/ask-with-file", methods=["POST"])
def ask_with_file():
    data = request.get_json()
    query = data.get("query", "")
    file_content = data.get("file_content", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Combine file content with query
    combined_query = f"Based on this document:\n\n{file_content}\n\nQuestion: {query}"

    start_time = time.time()
    result = pipeline.run(combined_query)
    response_time = round(time.time() - start_time, 2)

    log = QueryLog(
        query=query,
        decision=result["decision"],
        confidence=result["confidence"],
        boundary=result["boundary"],
        response=result["response"],
        response_time=response_time
    )
    db.session.add(log)
    db.session.commit()

    result["response_time"] = response_time
    result["id"] = log.id
    return jsonify(result)

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    log = db.session.get(QueryLog, data.get("id"))
    if log:
        log.feedback = data.get("feedback")
        db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/analytics", methods=["GET"])
def get_analytics():
    total    = db.session.query(func.count(QueryLog.id)).scalar()
    answer   = db.session.query(func.count(QueryLog.id)).filter(QueryLog.decision == "ANSWER").scalar()
    clarify  = db.session.query(func.count(QueryLog.id)).filter(QueryLog.decision == "CLARIFY").scalar()
    abstain  = db.session.query(func.count(QueryLog.id)).filter(QueryLog.decision == "ABSTAIN").scalar()
    escalate = db.session.query(func.count(QueryLog.id)).filter(QueryLog.decision == "ESCALATE").scalar()
    return jsonify({
        "total":    total,
        "ANSWER":   answer,
        "CLARIFY":  clarify,
        "ABSTAIN":  abstain,
        "ESCALATE": escalate
    })

@app.route("/history", methods=["GET"])
def get_history():
    logs = db.session.query(QueryLog).order_by(QueryLog.timestamp.desc()).all()
    return jsonify([l.to_dict() for l in logs])

@app.route("/evaluation")
def evaluation():
    return render_template("evaluation.html")

@app.route("/apidocs")
def apidocs():
    return render_template("apidocs.html")
@app.route("/export-csv", methods=["GET"])
def export_csv():
    logs = db.session.query(QueryLog).order_by(QueryLog.timestamp.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        "ID", "Query", "Decision", "Confidence",
        "Boundary", "Response", "Response Time",
        "Feedback", "Timestamp"
    ])

    # Data rows
    for log in logs:
        writer.writerow([
            log.id,
            log.query,
            log.decision,
            log.confidence,
            log.boundary,
            log.response,
            log.response_time,
            log.feedback or "None",
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=query_history.csv"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)