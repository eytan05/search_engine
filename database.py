import os
import psycopg2
from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st
from embedding import get_embedding
import PyPDF2
import nltk
from typing import Dict, List, Union


def create_documents_table(config: Dict) -> None:
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


def add_pdf_document(file: Union[UploadedFile, str]) -> str:
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf.pages)):
        text += pdf.pages[page_num].extract_text()
    return text


def add_document(doc_title: str, doc_text: str, config: Dict) -> None:
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        cur = conn.cursor()
        doc_text = doc_text.replace("�", "'")
        doc_text = doc_text.replace("\n", " ")
        text_list = split_text_into_triples(doc_text)
        if not check_documents_already_in(doc_title, config):
            for paragraph_num, paragraph_text in enumerate(text_list):
                if paragraph_text.strip() == "":
                    continue
                embedding = get_embedding(paragraph_text)
                cur.execute(
                    """
                    INSERT INTO documents (doc_title, paragraph_num, paragraph_text, paragraph_embedding)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (doc_title, paragraph_num, paragraph_text, embedding.tobytes()),
                )

            conn.commit()
        cur.close()
    conn.close()


def split_text_into_triples(text: str) -> List:
    sentences = nltk.tokenize.sent_tokenize(text)
    triples = [" ".join(sentences[i : i + 3]) for i in range(0, len(sentences), 3)]
    return triples


def drop_tables_documents(config: Dict) -> None:
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        cur = conn.cursor()
        cur.execute("""DROP table documents""")
        conn.commit()
        cur.close()
    conn.close()


def add_all_files_from_folder(folder_path: str, config: Dict) -> None:
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if ".txt" in file:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                file_text = f.read()
        elif file[-3:] == "pdf":
            file_text = add_pdf_document(file_path)
        else:
            print("format not supported")
            continue
        add_document(file, file_text, config)
        st.write(f"{file} uploaded")


def check_documents_already_in(filename: str, config: Dict) -> bool:
    with psycopg2.connect(
        database=config["db_name"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    ) as conn:
        cur = conn.cursor()
        filename = filename.replace("'", " ")
        query = f"SELECT * from documents where doc_title = '{filename}';"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        if not result:
            return False
        return True
