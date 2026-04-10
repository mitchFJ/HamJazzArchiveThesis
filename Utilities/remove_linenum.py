import fitz
from glob import glob
from pathlib import Path
import json

def redact(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    doc.delete_page(0)
    rect1 = fitz.Rect(0,0,60,1000)
    rect2 = fitz.Rect(0,720, 1000, 1100)
    for page in doc.pages():
        page.add_redact_annot(rect1)

        page.apply_redactions()

        page.add_redact_annot(rect2)

        page.apply_redactions()

    doc.save(output_path, garbage=3, deflate=True)
    doc.close()

def man_only_redact(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    rect1 = fitz.Rect(0,0,60,1000)
    rect2 = fitz.Rect(0,720, 1000, 1100)
    rect3 = fitz.Rect(0, 0, 1000, 270)
    for page in doc.pages():
        page.add_redact_annot(rect1)

        page.apply_redactions()

        page.add_redact_annot(rect2)

        page.apply_redactions()

        page.add_redact_annot(rect3)

        page.apply_redactions()

    doc.save(output_path, garbage=3, deflate=True)
    doc.close()

def redact_all(data):
    for pdf in data:
        input_file = pdf["path"][:16] + pdf["path"][23:]
        output = pdf["path"]
        if ("Audiovisual Materials" in pdf["type"]):
            redact(input_file, output)
        else:
            man_only_redact(input_file, output)

if __name__ == "__main__":
    with open("Data/doc_list.json", "r") as file:
        data = json.load(file)
    redact_all(data)