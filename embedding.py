from typing import Any
from transformers import AutoTokenizer, AutoModel
import torch


def get_embedding(text: str, model_name: str = "distilbert-base-uncased") -> Any:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state
    embeddings = embeddings.mean(dim=1)
    return embeddings.detach().numpy()
