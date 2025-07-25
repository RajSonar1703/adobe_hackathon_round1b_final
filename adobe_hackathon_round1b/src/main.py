import os
import json
from datetime import datetime
from utils import extract_sections
from processor import rank_sections

INPUT_DIR = "input"
OUTPUT_DIR = "output"

persona = "Raj Sonar"
job = "Student"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

timestamp = datetime.now().isoformat()
for file in os.listdir(INPUT_DIR):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(INPUT_DIR, file)
        sections = extract_sections(pdf_path)
        ranked = rank_sections(sections, persona, job)

        result = {
            "metadata": {
                "documents": [file],
                "persona": persona,
                "job": job,
                "timestamp": timestamp
            },
            "sections": ranked,
            "subsections": [
                {
                    "document": file,
                    "page": sec["page"],
                    "refined_text": sec["title"]
                } for sec in ranked
            ]
        }

        with open(os.path.join(OUTPUT_DIR, f"{file.replace('.pdf', '')}.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Processed: {file}")
