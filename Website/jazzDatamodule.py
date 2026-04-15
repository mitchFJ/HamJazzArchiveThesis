from pypdf import PdfReader

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from pathlib import Path
#import filter_sys

# Website Communication Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import json

# Websire Communication Setup - App and CSV path
app = Flask(__name__)
CORS(app)

# --- TEMPORARY FIX/TEST: filtering_label_list.py ---
label_list_file_path = '../Data/scraped_labels.txt'

def set_doc_to_labels(doc, label_dict):
    # print(doc)
    for label in doc['subject_topical']:
        key = label[:label.find(',')]
        if len(label_dict[key]) < 1:
            new_doc_list = [doc]
        else:
            new_doc_list = label_dict[key]
            new_doc_list.append(doc)
        label_dict.update({key: new_doc_list})
    return

def create_label_dict():
    label_dict = {}

    with open(label_list_file_path) as f:
        labels_list = f.readlines()
    
    for label in labels_list:
        if '\n' in label:
            label = label[:len(label) - 1]
        label = '\"label\":\"' + label + '\"'
        label_dict.update({label: []})

    return label_dict

def link_label_to_docs(doc_list, label_dict = create_label_dict()):
    for doc in doc_list:
        set_doc_to_labels(doc, label_dict)
    return label_dict
# --- End filtering_label_list.py ---

# --- TEMPORARY FIX/TEST: filter_sys.py ---
def get_doc_list(input_file_path):
    with open(input_file_path, mode='r') as f:
        data = json.load(f)

    return data

# Filters out the document list
def check_include(new_doc_list, label_list, label_dict):
    # Checks through each doc to see if a label is in the doc_list
    for label in label_list:
        label = '\"label\":\"' + label + '\"'
        
        for doc in label_dict[label]:
            if doc not in new_doc_list:
                new_doc_list.append(doc)

    return

# Filters out the document list
def check_exclude(new_doc_list, label_list, label_dict):
    # Checks through each doc to see if a label is in the doc_list
    for label in label_list:
        label = '\"label\":\"' + label + '\"'

        for doc in label_dict[label]:
            if doc in new_doc_list:
                new_doc_list.remove(doc)

    return

# Checks to see if there are any filters active in the documents
def filter_docs(include_list = [], exclude_list = ['jazz']): # Are the lists files or lists?
    new_doc_list = []
    doc_list = get_doc_list('../Data/doc_list.json')
    label_dict = link_label_to_docs(doc_list)

    # Checks if both filter lists have no elements
    if len(include_list) < 1:
        new_doc_list = doc_list
    else:
        check_include(new_doc_list, include_list, label_dict)
    
    # Check if documents have exclude filters
    if len(exclude_list) >= 1:
        check_exclude(new_doc_list, exclude_list, label_dict)
    
    return new_doc_list

def create_txt(doc_list):
    new_file_name = '../Data/filtered_doc_list.json'

    with open(new_file_name, 'w') as file:
        file.write("\n".join(doc_list))
    
    return
# --- End filter_sys.py ---

# Search funct class - BEGIN
NUM_RETURN = 5
URL_START = "https://litsdigital.hamilton.edu/do/"
PAGE_SELECT = "#page/"

class jazzDataModule():
    def __init__(self, include_list = [], exclude_list = []):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.get_filtered(include_list, exclude_list)

    def get_filtered(self, include_list = [], exclude_list = []):
        csv_file = Path("../Data/extracted_text.csv")
        db = pd.read_csv(csv_file)
        sentences = db["text"]
        page_list = db["pagenum"]
        url_list = db["url"]
        name_list = db["name"]

        encode_file = Path("../Data/embeddings.npy")
        encode_list = np.load(encode_file)

        valid_pdfs = filter_docs(include_list, exclude_list)
        with open("../Data/data_line_num.json", "r") as file:
            data = json.load(file)
        self.sentences = []
        self.page_list = []
        self.url_list = []
        self.encode_list = []
        self.name_list = []
        # print("------TEST-------")
        for pdf in valid_pdfs:
            # print(type(pdf))
            for i in data[pdf["path"]]:
                self.sentences.append(sentences[i])
                self.page_list.append(page_list[i])
                self.encode_list.append(encode_list[i])
                self.url_list.append(URL_START + url_list[i] + PAGE_SELECT)
                self.name_list.append(name_list[i])

    def evaluate_query(self, query):
        query_encode = self.tokenize(query).astype(np.float64)
        
        self.best_respones = [0 for i in range(NUM_RETURN)]
        self.best_pages = ["" for i in range(NUM_RETURN)]
        self.best_sentences = ["" for i in range(NUM_RETURN)]
        self.best_url = ["" for i in range(NUM_RETURN)]
        self.best_display = ["" for i in range(NUM_RETURN)]
        
        for i in range(len(self.encode_list)):
            similar = util.cos_sim(query_encode, self.encode_list[i])
            if (similar > self.best_respones[-1]):
                self.insert_response(i, similar)
        response = []
        for i in range(len(self.best_respones)):
            if (self.best_pages[i][0] == "["):
                this_response = [self.best_display[i], self.best_url[i] + self.best_pages[i][1:self.best_pages[i].find(",")], self.best_pages[i], self.best_sentences[i]]
            else:
                this_response = [self.best_display[i], self.best_url[i] + self.best_pages[i], self.best_pages[i], self.best_sentences[i]]
            response.append(this_response)
        return response

    def insert_response(self, index, similar):
        for i in range(len(self.best_respones)):
            if similar > self.best_respones[i]:
                self.best_respones.insert(i, similar)
                self.best_respones.pop()
                self.best_pages.insert(i,self.page_list[index])
                self.best_pages.pop()
                self.best_sentences.insert(i, self.sentences[index])
                self.best_sentences.pop()
                self.best_url.insert(i, self.url_list[index])
                self.best_url.pop()
                self.best_display.insert(i, self.name_list[index])
                self.best_display.pop()
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

def search_with_filters(query,inc_pass,exc_pass):
    test = jazzDataModule(inc_pass,exc_pass)
    print("Beginning filtered search...")
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
        global NUM_RETURN
        NUM_RETURN = request.json.get("glob_num_ret")
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
            #results = search_only_query(data)
            results = search_with_filters(data,inc_list_q,exc_list_q)
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