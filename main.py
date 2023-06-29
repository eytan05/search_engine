from dotenv import load_dotenv
from database import (
    add_document,
    create_documents_table,
    add_pdf_document,
    drop_tables_documents,
    add_all_files_from_folder,
)
import os
from get_guardian_article import get_article
from search_engine import get_documents, search
import streamlit as st
import nltk

load_dotenv()

config = {
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "db_name": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "port": os.getenv("PORT"),
    "guardian_api_key": os.getenv("GUARDIAN_API_KEY"),
}

nltk.download("punkt")


def upload_document() -> None:
    st.title("Upload Document")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
    if uploaded_file is not None:
        file_title = uploaded_file.name
        filetype = uploaded_file.type.split("/")[-1]
        if filetype.lower() == "pdf":
            doc_text = add_pdf_document(uploaded_file)
        else:
            doc_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        add_document(file_title, doc_text, config)
        st.write("File uploaded successfully!")
    folder_path = st.text_input("Enter the path to your folder")
    if st.button("Download all documents"):
        add_all_files_from_folder(folder_path, config)


def search_document() -> None:
    st.title("Search Documents")
    query = st.text_input("Enter your query")
    if st.button("Search"):
        results = search(query, 5, config)
        for result in results:
            st.write(f"Result: {result}")


def view_documents() -> None:
    st.title("View Documents")
    df = get_documents(config)
    st.dataframe(df)
    if st.button("Drop table"):
        drop_tables_documents(config)


def main() -> None:
    create_documents_table(config)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Upload Document",
            "Search",
            "View Documents",
            "Download Guardian Articles",
        ],
    )
    if page == "Home":
        st.title("Home Page")
        st.write("Welcome to the Home Page")
    elif page == "Upload Document":
        upload_document()
    elif page == "Download Guardian Articles":
        get_article(config)
    elif page == "Search":
        search_document()
    elif page == "View Documents":
        view_documents()


if __name__ == "__main__":
    main()
