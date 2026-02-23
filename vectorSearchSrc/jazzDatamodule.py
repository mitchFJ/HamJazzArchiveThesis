#import numpy as np
#import re
#from transformers import BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch

from pypdf import PdfReader

class jazzDataModule():
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        #tests = ["jazz is my favorite", "I love jazz"]
        #encoding = self.tokenize(tests)
        #print(util.cos_sim(encoding[0], encoding[1]))

    def evaluate_query(self, query):
        best_respone = 0
        best_sentence = ""
        best_pdf = ""
        input_pdf = Path("Transcripts/output/").glob("*.pdf")
        num = 0
        for pdf in input_pdf:
            num += 1
            print(num)
            text = self.exctract_text_from_pdf(pdf).split('MR: ')
            sentences = [query.strip()]
            for sentence in text:
                sentences.append(sentence.strip())
            encode = self.tokenize(sentences)
            for i in range(1, len(encode)):
                similar = util.cos_sim(encode[0], encode[i])
                if (similar > best_respone):
                    print(f"similar: {similar}, best: {best_respone}")
                    print(sentences[i])
                    best_respone = similar
                    best_pdf = pdf
                    best_sentence = sentences[i]
            #This is a run to make sure we don't take too long
            #for real cases we will want another algorithm (maybe key word search or fuzzy search)
            #to limit the transcripts we look through
            if (num > 20):
                break
        
        print(best_pdf)
        print(best_sentence)
        print(best_respone)


    def tokenize(self, text):
        encoding = self.model.encode(text)
        return encoding
    
    def exctract_text_from_pdf(self, path):
        reader = PdfReader(path)
        full_text = ""
        num_page = len(reader.pages)
        for i in range(1, num_page):
            page = reader.pages[i]
            full_text += page.extract_text()
        return full_text

print("A")
test = jazzDataModule()
test.evaluate_query("Leanring Jazz in an academic setting")