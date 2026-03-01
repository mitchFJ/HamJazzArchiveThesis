from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import pandas as pd

from pypdf import PdfReader

class jazzDataModule():
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def evaluate_query(self, query):
        df = pd.read_csv("extracted_text.csv")
        sentences = [query]
        sentences.extend(df["Text"])
        pdf_list = df["File"]
        page_list = df["Pagenum"]
        encode = self.tokenize(sentences)
        best_respone = 0
        best_pdf = ""
        best_page = ""
        best_sentence = ""
        for i in range(1, len(encode)):
            similar = util.cos_sim(encode[0], encode[i])
            if (similar > best_respone):
                best_respone = similar
                best_pdf = pdf_list[i]
                best_page = page_list[i]
                best_sentence = sentences[i]
        print(best_pdf)
        print(best_page)
        print(best_sentence)
        print(best_respone)


    def tokenize(self, text):
        encoding = self.model.encode(text)
        return encoding

if __name__ == "__main__":
    test = jazzDataModule()
    test.evaluate_query("Experiencing racism while playing")