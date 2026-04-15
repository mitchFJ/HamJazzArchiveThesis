from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from pathlib import Path
import json
import filter_sys

NUM_RETURN = 2
URL_START = "https://litsdigital.hamilton.edu/do/"
PAGE_SELECT = "#page/"

class jazzDataModule():
    def __init__(self, include_list = [], exclude_list = []):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.get_filtered(include_list, exclude_list)

    def get_filtered(self, include_list = [], exclude_list = []):
        csv_file = Path("Data/extracted_text.csv")
        db = pd.read_csv(csv_file)
        sentences = db["text"]
        page_list = db["pagenum"]
        url_list = db["url"]
        name_list = db["name"]

        encode_file = Path("Data/embeddings.npy")
        encode_list = np.load(encode_file)

        valid_pdfs = filter_sys.filter_docs(include_list, exclude_list)
        with open("Data/data_line_num.json", "r") as file:
            data = json.load(file)
        self.sentences = []
        self.page_list = []
        self.url_list = []
        self.encode_list = []
        self.name_list = []
        for pdf in valid_pdfs:
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

if __name__ == "__main__":
    test = jazzDataModule()
    query = input("Input your query: ")
    print(test.evaluate_query(query))