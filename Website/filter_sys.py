# File is extraneous at this point - useful for development, but necessary content is transferred to jazzDataModule.py or app.py

import filtering_label_list as fll
import json

def get_doc_list(input_file_path):
    with open(input_file_path, mode='r') as f:
        data = json.load(f)

    return data

# Filters out the document list
def check_include(new_doc_list, label_list, label_dict):
    # Checks through each doc to see if a label is in the doc_list
    for label in label_list:
        label = '\"label\":\"' + label + '\"'
        
        for doc in label_dict[label]:
            if doc not in new_doc_list:
                new_doc_list.append(doc)

    return

# Filters out the document list
def check_exclude(new_doc_list, label_list, label_dict):
    # Checks through each doc to see if a label is in the doc_list
    for label in label_list:
        label = '\"label\":\"' + label + '\"'

        for doc in label_dict[label]:
            if doc in new_doc_list:
                new_doc_list.remove(doc)

    return

# Checks to see if there are any filters active in the documents
def filter_docs(include_list = [], exclude_list = []): # Are the lists files or lists?
    doc_list = get_doc_list('../Data/doc_list.json')
    new_doc_list = []
    label_dict = fll.link_label_to_docs(doc_list)

    # Checks if both label lists have matching labels
    match_label_list = list(set(include_list).intersection(exclude_list))
    if len(match_label_list) > 0:
        for label in match_label_list:
            include_list.remove(label)
            exclude_list.remove(label)

    # Checks if include filter list has no elements
    if len(include_list) < 1:
        new_doc_list = doc_list
    else:
        check_include(new_doc_list, include_list, label_dict)
    
    # Check if exclude filter list has elements
    if len(exclude_list) > 0:
        check_exclude(new_doc_list, exclude_list, label_dict)
    
    return new_doc_list

def create_txt(doc_list):
    new_file_name = 'Data/filtered_doc_list.json'

    with open(new_file_name, 'w') as file:
        file.write("\n".join(doc_list))
    
    return