from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

from pypdf import PdfReader

class jazzDataModule():
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def evaluate_query(self, query):
        best_respone = 0
        best_sentence = ""
        best_pdf = ""
        input_pdf = Path("Transcripts/output/").glob("*.pdf")
        num = 0
        sentences = [query]
        pdf_list = [0]
        for pdf in input_pdf:
            num += 1
            text = self.exctract_text_from_pdf(pdf).split('MR: ')
            sentences.extend(text)
            for i in range(len(text)):
                pdf_list.append(pdf)
            #Currently, running this is too slow, but if we precomutate the data, the actual time spent
            #to do the vector search is fast, may be doable without another search algorithm
            if (num > 20):
                break
        encode = self.tokenize(sentences)
        for i in range(1, len(encode)):
            similar = util.cos_sim(encode[0], encode[i])
            if (similar > best_respone):
                #print(f"similar: {similar}, best: {best_respone}")
                #print(sentences[i])
                best_respone = similar
                best_pdf = pdf_list[i]
                best_sentence = sentences[i]
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

test = jazzDataModule()
test.evaluate_query("Dealing with racism while performing")