# Filter System for Website
import csv

# To find docs
csv_file_path = 'Data/Jazz_Interviews - Jazz_Interviews.csv'
label_list_file_path = 'Utilities/scraped_labels.txt'

doc_identifier = 'local_identifier'
labels_name = 'subject_topical'

# Gives the document path in the project
def get_doc_path(doc_identifier):
    doc_path = "Data/Transcripts/output/"
    ext = ".pdf"

    return doc_path + doc_identifier + ext

def get_label_list(doc):
    label_str = doc[2:len(doc) - 2]
    labels_list = label_str.split('},{')
    return labels_list

# Gets the documents from the CSV
def get_docs():
    doc_list = []

    with open(csv_file_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            doc_path = get_doc_path(row[doc_identifier][2:len(row[doc_identifier]) - 2])
            label_list = get_label_list(row[labels_name])
            doc_list.append(dict(path = doc_path, subject_topical = label_list))

    return doc_list

def set_doc_to_labels(doc, label_dict):
    for label in doc['subject_topical']:
        key = label[:label.find(',')]
        if len(label_dict[key]) < 1:
            new_doc_list = [doc['path']]
        else:
            new_doc_list = label_dict[key]
            new_doc_list.append(doc['path'])
        label_dict.update({key: new_doc_list})
    return

def create_label_dict():
    label_dict = {}

    with open(label_list_file_path) as f:
        labels_list = f.readlines()
    
    for label in labels_list:
        if '\n' in label:
            label = label[:len(label) - 1]
        label = '"label":"' + label + '"'
        label_dict.update({label: []})

    return label_dict

def link_label_to_docs(doc_list = get_docs(), label_dict = create_label_dict()):
    for doc in doc_list:
        set_doc_to_labels(doc, label_dict)
    return label_dict