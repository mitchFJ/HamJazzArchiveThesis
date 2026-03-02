from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import pandas as pd

from pypdf import PdfReader

# Website Communication Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import csv

# Websire Communication Setup - App and CSV path
app = Flask(__name__)
CORS(app)
CSV_PATH = '../extracted_text.csv'

class jazzDataModule():
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def evaluate_query(self, query):
        df = pd.read_csv(CSV_PATH)
        self.sentences = [query]
        self.sentences.extend(df["Text"])
        self.pdf_list = df["File"]
        self.page_list = df["Pagenum"]
        print("Tokenizing...")
        encode = self.tokenize(self.sentences)
        self.best_respones = [0, 0, 0, 0, 0]
        self.best_pdfs = ["", "", "", "", ""]
        self.best_pages = ["", "", "", "", ""]
        self.best_sentences = ["", "", "", "", ""]
        print("Checking for similar...")
        for i in range(1, len(encode)):
            similar = util.cos_sim(encode[0], encode[i])
            if (similar > self.best_respones[-1]):
                self.insert_response(i, similar)
        print("Formulating response...")
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
                self.best_pdfs.insert(i, self.pdf_list[index - 1])
                self.best_pdfs.pop()
                self.best_pages.insert(i,self.page_list[index - 1])
                self.best_pages.pop()
                self.best_sentences.insert(i, self.sentences[index])
                self.best_sentences.pop()
                return

    def tokenize(self, text):
        encoding = self.model.encode(text)
        return encoding

def search_only_query(query):
    test = jazzDataModule()
    print("Beginning search...")
    results_of_search = test.evaluate_query(query)
    return results_of_search

# The handler for communication events
@app.route('/run_search_funct', methods=['GET', 'POST'])
def run_search_funct():
    if request.method == 'POST':
        # Process data sent from JavaScript
        data = request.json.get("message")
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        else:
            print(data)
            results = search_only_query(data)
            print("Done searching.")
            if len(results)>0:
                return jsonify({"answer": results})
            else:
                return jsonify({"answer": "Length of resulting lol was 0."})
    else:
        # Handle GET request
        return jsonify({"message": "Hello from jazzDatamodule.py!"})

if __name__ == "__main__":
    # Run the server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)