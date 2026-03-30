from pypdf import PdfReader
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer, util
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from remove_linenum import redact_all

def save_text():
    cred = credentials.Certificate("fillius-jazz-archive-search-firebase-adminsdk-fbsvc-cda02f015f.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://fillius-jazz-archive-search-default-rtdb.firebaseio.com'})
    ref = db.reference('/')
    input_pdf = Path("Data/Transcripts/output/").glob("*.pdf")
    key = 0
    for pdf in input_pdf:
        all_text = []
        all_pdf = []
        all_pages = []
        page = 2
        text = re.split("[A-Z]{2}:", exctract_text_from_pdf(pdf))
        for i in range(len(text)):
            all_text.append(text[i].strip())
            all_pdf.append(pdf)
            if ("\n" in text[i]):
                all_pages.append((page, page+1))
                page += 1
            else:
                all_pages.append(page)

        encoding = tokenize(all_text)

        grouped_text = {}
        for i in range(len(all_text)):
            grouped_text[key + i] = [all_text[i], encoding[i].tolist(), str(all_pdf[i]), all_pages[i]]
        key += len(all_text)

        ref.update(grouped_text)

def tokenize(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoding = model.encode(text)
    return encoding



def exctract_text_from_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    num_page = len(reader.pages)
    for i in range(1, num_page):
        page = reader.pages[i]
        full_text += page.extract_text()
        full_text += "\n"
    return full_text

if __name__ == "__main__":
    redact_all()
    save_text()