from pypdf import PdfReader
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from remove_linenum import redact_all
import pandas as pd
import json

def save_text():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    cred = credentials.Certificate("Data/fillius-jazz-archive-search-firebase-adminsdk-fbsvc-cda02f015f.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://fillius-jazz-archive-search-default-rtdb.firebaseio.com'})
    ref = db.reference('/')
    key = 0
    with open("Data/doc_list.json", "r") as file:
        pdfs = json.load(file)
    for pdf in pdfs:
        all_text = []
        all_pdf = []
        all_pages = []
        node_id = []
        display_name = []
        page = 1
        if ("Audiovisual Materials" in pdf["type"]):
            page = 2
        text = re.split("[A-Z]{2}:", exctract_text_from_pdf(pdf["path"]))
        for i in range(1, len(text)):
            all_text.append(text[i].strip())
            all_pdf.append(pdf["path"])
            node_id.append(pdf["id"])
            display_name.append(pdf["name"])
            if ("\n" in text[i]):
                all_pages.append((page, page+1))
                page += 1
            else:
                all_pages.append(page)

        encoding = tokenize(all_text, model)

        grouped_text = {}
        for i in range(len(all_text)):
            grouped_text[key + i] = [all_text[i], encoding[i].tolist(), str(all_pdf[i]),
                                     all_pages[i], node_id[i], display_name[i]]
        key += len(all_text)

        ref.update(grouped_text)

def tokenize(text, model):
    encoding = model.encode(text)
    return encoding

def exctract_text_from_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
        full_text += "\n"
    return full_text

if __name__ == "__main__":
    #redact_all()
    save_text()