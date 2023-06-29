from dotenv import load_dotenv
from database import add_document, create_documents_table, add_pdf_document
import os
from search_engine import get_documents, search
import streamlit as st

load_dotenv()

config = {
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "db_name": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "port": os.getenv("PORT"),
}


def main():
    create_documents_table(config)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", ["Home", "Upload Document", "Search", "View Documents"]
    )
    if page == "Home":
        st.title("Home Page")
        st.write("Welcome to the Home Page")
    elif page == "Upload Document":
        st.title("Upload Document")
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
        if uploaded_file is not None:
            file_title = uploaded_file.name
            filetype = uploaded_file.type.split("/")[-1]
            if filetype.lower() == "pdf":
                doc_text = add_pdf_document(uploaded_file)
            else:
                doc_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            doc_text = doc_text.replace("\n", " ")
            add_document(file_title, doc_text, config)
            st.write("File uploaded successfully!")
    elif page == "Search":
        st.title("Search Documents")
        query = st.text_input("Enter your query")
        if st.button("Search"):
            results = search(query, 3, config)
            for result in results:
                st.write(f"Result: {result}")
    elif page == "View Documents":
        st.title("View Documents")
        df = get_documents(config)
        st.dataframe(df)


if __name__ == "__main__":
    main()