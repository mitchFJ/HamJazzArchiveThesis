import csv
from pypdf import PdfReader
from pathlib import Path

def save_text():
    input_pdf = Path("Transcripts/output/").glob("*.pdf")
    text_list = []
    pdf_list = []
    page_list = []
    num = 0
    for pdf in input_pdf:
        page = 2
        num += 1
        print(num)
        text = exctract_text_from_pdf(pdf).split('MR: ')
        for i in range(len(text)):
            text_list.append(text[i].strip())
            pdf_list.append(pdf)
            if ("\n" in text[i]):
                page_list.append((page, page+1))
                page += 1
            else:
                page_list.append(page)
    saved_data = [pdf_list, text_list, page_list]

    with open("extracted_text.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(saved_data)


def exctract_text_from_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    num_page = len(reader.pages)
    for i in range(1, num_page):
        page = reader.pages[i]
        full_text += page.extract_text()
        full_text += "\n"
    return full_text

if __name__ == "__main__":
    save_text()