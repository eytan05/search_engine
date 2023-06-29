import psycopg2
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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


def search(query, top_k, config):
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
