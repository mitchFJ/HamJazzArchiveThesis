from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import pandas as pd

NUM_RETURN = 5

class jazzDataModule():
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def evaluate_query(self, query):
        df = pd.read_csv("extracted_text.csv")
        self.sentences = [query]
        self.sentences.extend(df["Text"])
        self.pdf_list = df["File"]
        self.page_list = df["Pagenum"]
        encode = self.tokenize(self.sentences)

        self.best_respones = [0 for i in range(NUM_RETURN)]
        self.best_pdfs = ["" for i in range(NUM_RETURN)]
        self.best_pages = ["" for i in range(NUM_RETURN)]
        self.best_sentences = ["" for i in range(NUM_RETURN)]
        
        for i in range(1, len(encode)):
            similar = util.cos_sim(encode[0], encode[i])
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

if __name__ == "__main__":
    test = jazzDataModule()
    print(test.evaluate_query("Experiencing racism while playing"))