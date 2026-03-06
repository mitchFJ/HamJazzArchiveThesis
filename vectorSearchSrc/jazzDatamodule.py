from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

NUM_RETURN = 5

class jazzDataModule():
    def __init__(self):
        cred = credentials.Certificate("fillius-jazz-archive-search-firebase-adminsdk-fbsvc-cda02f015f.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://fillius-jazz-archive-search-default-rtdb.firebaseio.com'})
        ref = db.reference('/')

        self.sentences = []
        self.encode_list = []
        self.pdf_list = []
        self.page_list = []
        last_key = 0
        
        while True:
            docs = ref.order_by_key().start_at(str(last_key)).limit_to_first(30000)
            
            segment = docs.get()
            if segment == None:
                break

            for i in range(last_key, len(segment)):
                self.sentences.append(segment[i][0])
                self.encode_list.append(segment[i][1].copy())
                self.pdf_list.append(segment[i][2])
                self.page_list.append(segment[i][3])

            last_key += len(segment)
            print("page done")

        self.model = SentenceTransformer('all-MiniLM-L6-v2')

            

    def evaluate_query(self, query):
        df = pd.read_csv("extracted_text.csv")
        query_encode = self.tokenize(query)
        
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

if __name__ == "__main__":
    test = jazzDataModule()
    print(test.evaluate_query("Experiencing racism while playing"))