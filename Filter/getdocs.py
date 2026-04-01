# Filter System for Website
import csv

# To find docs
csv_file_path = 'Data/Jazz_Interviews - Jazz_Interviews.csv'
label_list_file_path = 'Utilities/scraped_labels.txt'

doc_identifier = 'local_identifier'
labels_name = 'subject_topical'

def link_label_to_docs():
    return

def create_label_map():
    return

# Gives the document path in the project
def get_doc_path(doc_identifier):
    doc_path = "Data/Transcripts/output/"
    ext = ".pdf"

    return doc_path + doc_identifier + ext

# Gets the documents from the CSV
def get_docs():
    doc_list = []

    with open(file_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            doc_path = get_doc_path(row[doc_identifier][2:len(row[doc_identifier]) - 2])
            doc_list.append(dict(path = doc_path, subject_topical = row[labels_name]))

    return doc_list