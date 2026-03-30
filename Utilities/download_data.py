import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pathlib import Path
import json


def download_data():
    cred = credentials.Certificate("Data/fillius-jazz-archive-search-firebase-adminsdk-fbsvc-cda02f015f.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://fillius-jazz-archive-search-default-rtdb.firebaseio.com'})
    ref = db.reference('/')

    sentences = []
    encode_list = []
    pdf_list = []
    page_list = []
    last_key = 0
    num = 0

    while True:
        num += 1
        docs = ref.order_by_key().start_at(str(last_key)).limit_to_first(30000)
        
        segment = docs.get()
        if segment == None:
            break

        for i in range(last_key, len(segment)):
            sentences.append(segment[i][0])
            encode_list.append(segment[i][1].copy())
            pdf_list.append(segment[i][2])
            page_list.append(segment[i][3])

        last_key += len(segment)
        print(f"{50 * num}% done")

    data = {"text": sentences,
        "pdf": pdf_list,
        "pagenum": page_list
    }
    csv_file = Path("Data/extracted_text.csv")
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    encode_file = Path("Data/embeddings.npy")
    np.save(encode_file, encode_list)
    current = pdf_list[0]
    page_nums = []
    make_json = {}
    for i in range(len(pdf_list)):
        if(current == pdf_list[i]):
            page_nums.append(i)
        else:
            make_json[current] = page_nums.copy()
            current = pdf_list[i]
            page_nums = [i]
    make_json[current] = page_nums.copy()
    with open("Data/data_line_num.json", "w") as f:
        json.dump(make_json, f, indent=4)

def just_json():
    csv_file = Path("Data/extracted_text.csv")
    db = pd.read_csv(csv_file)
    pdf_list = db["pdf"]
    current = pdf_list[0]
    page_nums = []
    make_json = {}
    for i in range(len(pdf_list)):
        if(current == pdf_list[i]):
            page_nums.append(i)
        else:
            make_json[current] = page_nums.copy()
            current = pdf_list[i]
            page_nums = [i]
    make_json[current] = page_nums.copy()
    with open("Data/data_line_num.json", "w") as f:
        json.dump(make_json, f, indent=4)

if __name__ == "__main__":
    download_data()
    #just_json()