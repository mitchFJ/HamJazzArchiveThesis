from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from pathlib import Path

NUM_RETURN = 5

class jazzDataModule():
    def __init__(self):
        csv_file = Path("Utilities/extracted_text.csv")
        db = pd.read_csv(csv_file)
        self.sentences = db["text"]
        self.pdf_list = db["pdf"]
        self.page_list = db["pagenum"]
        
        encode_file = Path("Utilities/embeddings.npy")
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

if __name__ == "__main__":
    test = jazzDataModule()
    print(test.evaluate_query("Experiencing racism while playing"))