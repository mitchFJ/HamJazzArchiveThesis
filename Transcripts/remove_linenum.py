import fitz
from glob import glob
from pathlib import Path

def redact(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    rect1 = fitz.Rect(0,0,60,1000)
    rect2 = fitz.Rect(0,750, 1000, 1100)
    for page in doc.pages():
        page.add_redact_annot(rect1)

        page.apply_redactions()

        page.add_redact_annot(rect2)

        page.apply_redactions()

    doc.save(output_path, garbage=3, deflate=True)
    doc.close()

if __name__ == "__main__":
    input_pdf = Path(".").glob("*.pdf")
    pdf_num = 1
    for pdf in input_pdf:
        output = "output/num"+str(pdf_num)+".pdf"
        redact(pdf, output)
        pdf_num += 1