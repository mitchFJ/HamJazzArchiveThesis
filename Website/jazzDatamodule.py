from pypdf import PdfReader

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from pathlib import Path

NUM_RETURN = 5

# Website Communication Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import json

# Websire Communication Setup - App and CSV path
app = Flask(__name__)
CORS(app)
CSV_PATH = '../extracted_text.csv'

# Search funct class - BEGIN
class jazzDataModule():
    def __init__(self):
        csv_file = Path("../Data/extracted_text.csv")
        db = pd.read_csv(csv_file)
        self.sentences = db["text"]
        self.pdf_list = db["pdf"]
        self.page_list = db["pagenum"]
        
        encode_file = Path("../Data/embeddings.npy")
        self.encode_list = np.load(encode_file)

        self.model = SentenceTransformer('all-MiniLM-L6-v2')

            

    def evaluate_query(self, query):
        query_encode = self.tokenize(query).astype(np.float64)
        
        self.best_respones = [0 for i in range(NUM_RETURN)]
        self.best_pdfs = ["" for i in range(NUM_RETURN)]
        self.best_pages = ["" for i in range(NUM_RETURN)]
        self.best_sentences = ["" for i in range(NUM_RETURN)]
        
        for i in range(len(self.encode_list)):
            similar = util.cos_sim(query_encode, self.encode_list[i])
            if (similar > self.best_respones[-1]):
                self.insert_response(i, similar)
        response = []
        for i in range(len(self.best_respones)):
            this_response = [self.best_pdfs[i], self.best_pages[i], self.best_sentences[i]]
            response.append(this_response)
        return response

    def insert_response(self, index, similar):
        for i in range(len(self.best_respones)):
            if similar > self.best_respones[i]:
                self.best_respones.insert(i, similar)
                self.best_respones.pop()
                self.best_pdfs.insert(i, self.pdf_list[index])
                self.best_pdfs.pop()
                self.best_pages.insert(i,self.page_list[index])
                self.best_pages.pop()
                self.best_sentences.insert(i, self.sentences[index])
                self.best_sentences.pop()
                return

    def tokenize(self, text):
        encoding = self.model.encode(text)
        return encoding
# Search funct class - END

# Search funct class activation
def search_only_query(query):
    test = jazzDataModule()
    print("Beginning query-only search...")
    results_of_search = test.evaluate_query(query)
    return results_of_search

# Filter-related code - BEGIN -
doc_name = 'label'
labels_name = 'subject_topical'

include_list = []
exclude_list = []

include_docs = []
exclude_docs = []

file_name = '../Data/Jazz_Interviews - Jazz_Interviews.csv'

def check_list(doc_list, new_doc_list, label_list, is_included):
    for row in doc_list:
        for label in label_list:
            if label in row[labels_name]:
                if is_included:
                    new_doc_list.append(dict(label = row[doc_name], subject_topical = row[labels_name]))
                break

            if not is_included:
                new_doc_list.append(dict(label = row[doc_name], subject_topical = row[labels_name]))
    return

# with open(file_name, newline='') as csv_file:
#     csv_reader = csv.DictReader(csv_file)

#     if len(include_list) > 0:
#         check_list(csv_reader, include_docs, include_list, True)
#     else:
#         for row in csv_reader:
#             include_docs.append(dict(label = row[doc_name], subject_topical = row[labels_name]))

# if len(exclude_list) > 0:
#     check_list(include_docs, exclude_docs, exclude_list, False)
# else:
#     exclude_docs = include_docs

def get_list_of_labels():
    label_list = []
    with open('../Data/scraped_labels.txt', 'r') as file:
        label_list = file.read().splitlines()
    # with open(file_name, newline='') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     for row in csv_reader:
    #         include_docs.append(dict(label = row[doc_name], subject_topical = row[labels_name]))
    #         print(row[labels_name])
    #         labels_here = json.loads(row[labels_name])
    #         for index in range(len(labels_here)):
    #             print(f"INDEXth: {labels_here[index]}")
    #             print(f"       : {labels_here[index]['label']}")
    #             if labels_here[index]['label'] not in label_list:
    #                 label_list.append(labels_here[index]['label'])
    #             else:
    #                 print("         -Already included.-")
    for label in label_list:
        print(label, end=', ')
    print()
    return label_list

# Filter-related code - END -

# The handler for communication events: Search
@app.route('/run_search_funct', methods=['GET', 'POST'])
def run_search_funct():
    if request.method == 'POST':
        # Process data sent from JavaScript
        data = request.json.get("message")
        inc_list_q = request.json.get("inc_list_json_ver")
        exc_list_q = request.json.get("exc_list_json_ver")
        if inc_list_q:
            print("Successfully passed includes...")
            for x in inc_list_q:
                print("   "+x)
        else:
            print("No include tags passed.")
        if exc_list_q:
            print("Successfully passed excludes...")
            for x in exc_list_q:
                print("   "+x)
        else:
            print("No exclude tags passed.")
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        else:
            print("Search query: "+data)
            results = search_only_query(data)
            print("Done searching.")
            if len(results)>0:
                return jsonify({"answer": results})
            else:
                return jsonify({"answer": "Length of resulting lol was 0."})
    else:
        # Handle GET request
        return jsonify({"message": "Hello from jazzDatamodule.py!"})

# Handler: Filters
@app.route('/run_filters_funct', methods=['GET', 'POST'])
def filters_funct():
    if request.method == 'GET':
        label_list_answer = get_list_of_labels()
        return jsonify({"answer": label_list_answer})
    elif request.method == 'POST':
        return
    else:
        return jsonify({"message": "Hello from jazzDatamodule.py - the filters!"})

if __name__ == "__main__":
    # Run the server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)