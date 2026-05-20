from pypdf import PdfReader
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer
from remove_linenum import redact_all
import json
import pandas as pd
import numpy as np


def save_text():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    with open("Data/doc_list.json", "r") as file:
        pdfs = json.load(file)
    all_text = []
    all_pdf = []
    all_pages = []
    node_id = []
    display_name = []
    for pdf in pdfs:
        page = 1
        if ("Audiovisual Materials" in pdf["type"]):
            page = 2
        text = re.split("[A-Z]{2}:", exctract_text_from_pdf(pdf["path"]))
        for i in range(1, len(text) - 1):
            all_text.append(text[i-1].strip() + "\n" + text[i].strip() + "\n" + text[i+1].strip())
            all_pdf.append(pdf["path"])
            node_id.append(pdf["id"])
            display_name.append(pdf["name"])
            if ("\n" in text[i]):
                all_pages.append((page, page+1))
                page += 1
            else:
                all_pages.append(page)
        num += 1

    encoding = tokenize(all_text, model)
    data = {"text": all_text,
        "pdf": all_pdf,
        "pagenum": all_pages,
        "url": node_id,
        "name": display_name
    }
    csv_file = Path("Data/extracted_text.csv")
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    encode_file = Path("Data/embeddings.npy")
    np.save(encode_file, encoding)
    current = all_pdf[0]
    page_nums = []
    make_json = {}
    for i in range(len(all_pdf)):
        if(current == all_pdf[i]):
            page_nums.append(i)
        else:
            make_json[current] = page_nums.copy()
            current = all_pdf[i]
            page_nums = [i]
    make_json[current] = page_nums.copy()
    with open("Data/data_line_num.json", "w") as f:
        json.dump(make_json, f, indent=4)


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
    save_text()