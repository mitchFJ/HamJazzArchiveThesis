import filtering_label_list as fll
import json

# Gets the information from doc list JSON file
def get_doc_dict(input_file_path):
    with open(input_file_path, mode='r') as f:
        data = json.load(f)

    return data

# Filters in documents that have the labels in the given label list
def check_include(new_doc_list, label_list, doc_list, label_dict):
    # Checks through each doc to see if a label is in the doc list
    for label in label_list:
        for doc in label_dict[label]:
            if doc_list[doc] not in new_doc_list:
                new_doc_list.append(doc_list[doc])
    return

# Filters out documents that have the labels in the given label list
def check_exclude(new_doc_list, label_list, doc_list, label_dict):
    # Checks through each doc to see if a label is in the doc_list
    for label in label_list:
        for doc in label_dict[label]:
            if doc_list[doc] in new_doc_list:
                new_doc_list.remove(doc_list[doc])
    return

# Checks to see if there are any filters active in the documents
def filter_docs(include_list = [], exclude_list = []):
    # Variables for the program to function
    new_doc_list = []
    doc_list = get_doc_dict('../Data/doc_list.json')
    label_dict = fll.link_label_to_docs(doc_list)

    # Checks if both filter lists have no elements
    ## Check if there are include filters
    if len(include_list) > 0:
        check_include(new_doc_list, include_list, doc_list, label_dict)
    ## Check if documents have exclude filters
    if len(exclude_list) > 0:
        check_exclude(new_doc_list, exclude_list, doc_list, label_dict)

    # Checks if the document list is empty
    if len(new_doc_list) < 1:
        new_doc_list = list(doc_list.values())
    
    return new_doc_list