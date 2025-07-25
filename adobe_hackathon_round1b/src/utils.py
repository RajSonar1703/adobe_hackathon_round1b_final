import fitz  # PyMuPDF

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text.split()) >= 5:
                sections.append({
                    "text": text,
                    "page": page_num
                })
    return sections
