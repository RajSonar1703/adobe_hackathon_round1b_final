from transformers import AutoTokenizer, AutoModel
import torch

model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def embed(text):
    tokens = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        output = model(**tokens)
    return output.last_hidden_state.mean(dim=1)

def rank_sections(sections, persona, job):
    query = f"{persona} wants to {job}"
    query_embedding = embed(query)

    for section in sections:
        section_embedding = embed(section["text"])
        score = torch.cosine_similarity(query_embedding, section_embedding).item()
        section["score"] = score
        section["title"] = section.pop("text")

    ranked = sorted(sections, key=lambda x: x["score"], reverse=True)
    for i, sec in enumerate(ranked[:5], 1):
        sec["importance_rank"] = i
        sec["document"] = ""  # set by main.py
    return ranked[:5]
