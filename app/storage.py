import json
import os


DATA_FILE = "documents.json"


def load_documents():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_documents(documents):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=2
        )