import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pathlib import Path
import json

NUM_IN = 30000


def download_data():
    cred = credentials.Certificate("Data/fillius-jazz-archive-search-firebase-adminsdk-fbsvc-cda02f015f.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://fillius-jazz-archive-search-default-rtdb.firebaseio.com'})
    ref = db.reference('/')

    sentences = []
    encode_list = []
    pdf_list = []
    page_list = []
    url_list = []
    display_name = []
    last_key = 0
    num = 0

    while True:
        docs = ref.order_by_key().start_at(str(last_key)).limit_to_first(NUM_IN)
        num += 1
        
        segment = docs.get()
        #print(len(segment))
        #print(segment)
        if not segment:
            break
        
        if last_key == 0 or last_key == 1:
            for results in segment[last_key:]:
                sentences.append(results[0])
                encode_list.append(results[1].copy())
                pdf_list.append(results[2])
                page_list.append(results[3])
                url_list.append(results[4])
                display_name.append(results[5])
        else:
            for results in segment.values():
                sentences.append(results[0])
                encode_list.append(results[1].copy())
                pdf_list.append(results[2])
                page_list.append(results[3])
                url_list.append(results[4])
                display_name.append(results[5])

        last_key += NUM_IN
        print(f"{50 * num}% done")
        if (num == 2):
            break

    data = {"text": sentences,
        "pdf": pdf_list,
        "pagenum": page_list,
        "url": url_list,
        "name": display_name
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