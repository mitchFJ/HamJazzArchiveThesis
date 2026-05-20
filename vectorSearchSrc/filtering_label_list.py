# Creates a label dictionary for the document paths to be stored
def create_label_dict(label_list_txt = '../Data/scraped_labels.txt'):
    label_dict = {}

    with open(label_list_txt) as f:
        labels_list = f.readlines()
    
    for label in labels_list:
        if '\n' in label:
            label = label[:len(label) - 1]
        label_dict.update({label: []})

    return label_dict

# Sets the doc path to the doc's corresponding labels in the label dictionary for ease of searching
def set_doc_to_labels(doc, doc_list, label_dict):
    for key in doc_list[doc]['subject_topical']:
        if len(label_dict[key]) < 1:
            new_doc_list = [doc]
        else:
            new_doc_list = label_dict[key]
            new_doc_list.append(doc)
        label_dict.update({key: new_doc_list})
    return

# Links each doc to each entry in the label dictionary
def link_label_to_docs(doc_list, label_dict = create_label_dict()):
    for doc in doc_list:
        set_doc_to_labels(doc, doc_list, label_dict)
    return label_dict