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
def filter_docs(doc_list, include_list = ['jazz'], exclude_list = ['composers']): # Are the lists files or lists?
    new_doc_list = []
    label_dict = fll.link_label_to_docs(doc_list)

    # Checks if both filter lists have no elements
    if len(include_list) < 1:
        new_doc_list = doc_list
    else:
        check_include(new_doc_list, include_list, label_dict)
    
    # Check if documents have exclude filters
    if len(exclude_list) >= 1:
        check_exclude(new_doc_list, exclude_list, label_dict)
    
    return new_doc_list

def create_txt(doc_list):
    new_file_name = 'Data/doc_list.txt'

    with open(new_file_name, 'w') as file:
        file.write("\n".join(doc_list))
    
    return

doc_list = get_doc_list('Data/doc_list.json')
filtered_docs = filter_docs(doc_list)
create_txt(filtered_docs)