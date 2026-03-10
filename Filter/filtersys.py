# Filter System for Website
import csv

doc_name = 'label'
labels_name = 'subject_topical'

include_list = []
exclude_list = []

include_docs = []
exclude_docs = []

file_name = 'Data/Jazz_Interviews - Jazz_Interviews.csv'

def check_list(doc_list, new_doc_list, label_list, is_included):
    for row in doc_list:
        for label in label_list:
            if label in row[labels_name]:
                if is_included:
                    new_doc_list.append(dict(label = row[doc_name], subject_topical = row[labels_name]))
                break

            if not is_included:
                new_doc_list.append(dict(label = row[doc_name], subject_topical = row[labels_name]))
    return

with open(file_name, newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    if len(include_list) > 0:
        check_list(csv_reader, include_docs, include_list, True)
    else:
        for row in csv_reader:
            include_docs.append(dict(label = row[doc_name], subject_topical = row[labels_name]))

if len(exclude_list) > 0:
    check_list(include_docs, exclude_docs, exclude_list, False)
else:
    exclude_docs = include_docs