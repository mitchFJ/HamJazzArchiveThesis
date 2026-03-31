# Filter System for Website
import csv

# To find docs
file_path = 'Data/Jazz_Interviews - Jazz_Interviews.csv'

doc_identifier = 'local_identifier'
labels_name = 'subject_topical'

# Filters out the document list
def check_list(doc_list, label_list, is_included):
    new_doc_list = []

    # Checks through each doc to see if a label is in the doc_list
    for doc in doc_list:
        # CITE: https://www.geeksforgeeks.org/python/python-test-if-string-contains-element-from-list/
        if any(label in doc['subject_topical'] for label in label_list):
            if is_included:
                new_doc_list.append(doc)
        else:
            if not is_included:
                new_doc_list.append(doc)

    return new_doc_list

# Checks to see if there are any filters active in the documents
def filter_docs(doc_list, include_list, exclude_list):
    new_doc_list = []

    # Checks if both filter lists have no elements
    if len(include_list) < 1 and len(exclude_list) < 1:
        new_doc_list = doc_list
        return new_doc_list

    # Check if documents have include filters
    if len(include_list) >= 1:
        new_doc_list = check_list(doc_list, include_list, True)
    
    # Check if documents have exclude filters
    if len(exclude_list) >= 1:
        new_doc_list = check_list(doc_list, exclude_list, False)
    
    return new_doc_list

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