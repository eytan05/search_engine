import psycopg2
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Tuple
import streamlit as st
from embedding import get_embedding
import pandas as pd


def get_documents(config):
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT doc_title, paragraph_num, paragraph_text, paragraph_embedding FROM documents;"
                )
            )
            documents = cur.fetchall()
            df = pd.DataFrame(
                documents,
                columns=[
                    "doc_title",
                    "paragraph_num",
                    "paragraph_text",
                    "paragraph_embedding",
                ],
            )
    return df


def search(query: str, top_k: int, config: Dict) -> List[Tuple]:
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        cur = conn.cursor()
        query_embedding = get_embedding(query)
        cur.execute(
            "SELECT doc_title, paragraph_num, paragraph_text, paragraph_embedding FROM documents"
        )
        results = cur.fetchall()
        similarities = []
        for doc_id, paragraph_num, paragraph_text, paragraph_embedding in results:
            paragraph_embedding = np.frombuffer(
                paragraph_embedding, dtype=np.float32
            ).reshape(1, -1)
            if paragraph_embedding.shape != query_embedding.shape:
                print(
                    f"Skipping paragraph {paragraph_num} in document {doc_id} due to shape mismatch."
                )
                continue

            similarity = cosine_similarity(query_embedding, paragraph_embedding)
            similarities.append(
                (doc_id, paragraph_num, paragraph_text, similarity[0][0])
            )
        similarities.sort(key=lambda x: x[3], reverse=True)
        return similarities[:top_k]


def change_color_text(t: Tuple) -> None:
    doc_id, paragraph_num, paragraph_text, similarity_score = t
    colored_paragraph_text = f"<span style='color:blue;'>{paragraph_text}</span>"
    new_tuple = (doc_id, paragraph_num, colored_paragraph_text, similarity_score)
    st.write(f"Result: {new_tuple}", unsafe_allow_html=True)
