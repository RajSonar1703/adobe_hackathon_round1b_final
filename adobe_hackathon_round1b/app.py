from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json
from src.utils import extract_sections
from src.processor import rank_sections
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_files = request.files.getlist('pdfs')
    persona = request.form.get('persona')
    job = request.form.get('job')
    persona_job = f"{persona} - {job}"

    output = {
        "metadata": {
            "persona": persona,
            "job": job,
            "timestamp": datetime.now().isoformat(),
            "documents": []
        },
        "sections": [],
        "subsections": []
    }

    for file in uploaded_files:
        filename = file.filename
        file_path = os.path.join("input", filename)
        file.save(file_path)

        sections = extract_sections(file_path)
        ranked = rank_sections(sections, persona_job)
        output["metadata"]["documents"].append(filename)

        for i, sec in enumerate(ranked[:5]):
            output["sections"].append({
                "document": filename,
                "page": sec["page"],
                "title": sec["text"],
                "importance_rank": i + 1
            })
            output["subsections"].append({
                "document": filename,
                "refined_text": sec["text"],
                "page": sec["page"]
            })

    return jsonify(output)

if __name__ == '__main__':
    if not os.path.exists("input"):
        os.mkdir("input")
    app.run(debug=True)

