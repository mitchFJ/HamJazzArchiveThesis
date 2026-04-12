label_list_file_path = 'Data/scraped_labels.txt'

def set_doc_to_labels(doc, label_dict):
    for label in doc['subject_topical']:
        key = label[:label.find(',')]
        if len(label_dict[key]) < 1:
            new_doc_list = [doc['path']]
        else:
            new_doc_list = label_dict[key]
            new_doc_list.append(doc)
        label_dict.update({key: new_doc_list})
    return

def create_label_dict():
    label_dict = {}

    with open(label_list_file_path) as f:
        labels_list = f.readlines()
    
    for label in labels_list:
        if '\n' in label:
            label = label[:len(label) - 1]
        label = '\"label\":\"' + label + '\"'
        label_dict.update({label: []})

    return label_dict

def link_label_to_docs(doc_list, label_dict = create_label_dict()):
    for doc in doc_list:
        set_doc_to_labels(doc, label_dict)
    return label_dict

