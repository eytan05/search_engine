import psycopg2
from embedding import get_embedding
import PyPDF2


def create_documents_table(config):
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        cur = conn.cursor()
        cur.execute(
            """
        CREATE TABLE if not exists documents (
            doc_title text,
            paragraph_num integer,
            paragraph_text text,
            paragraph_embedding bytea
        )
        """
        )
        conn.commit()
        cur.close()
    conn.close()


def add_pdf_document(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf.pages)):
        text += pdf.pages[page_num].extract_text()
    return text


def add_document(doc_title, doc_text, config):
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        cur = conn.cursor()
        chunks = chunk_text(doc_text, 60)

        for i, chunk in enumerate(chunks):
            if chunk.strip() == "":
                continue

            embedding = get_embedding(chunk)
            cur.execute(
                """
                INSERT INTO documents (doc_title, paragraph_num, paragraph_text, paragraph_embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (doc_title, i, chunk, embedding.tobytes()),
            )

        conn.commit()
        cur.close()
    conn.close()


def chunk_text(text, max_words):
    words = text.split()
    chunks = [
        " ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)
    ]
    return chunks