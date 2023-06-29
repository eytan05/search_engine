import requests
from bs4 import BeautifulSoup
import os
import re
import streamlit as st
from typing import Dict


def get_article(config: Dict) -> None:
    api_key = config["guardian_api_key"]
    api_url = (
        f"https://content.guardianapis.com/search?show-fields=body&api-key={api_key}"
    )
    response = requests.get(api_url)
    data = response.json()
    if not os.path.exists("documents"):
        os.makedirs("documents")

    for result in data["response"]["results"]:
        title = result["webTitle"]
        title = re.sub("[^a-zA-Z0-9 \n\.]", "", title)
        title_file = title[:50]
        content = result["fields"]["body"]
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text()
        with open(
            os.path.join("documents", f"{title_file}.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(text)
        st.write(f"Succefully download {title}")
