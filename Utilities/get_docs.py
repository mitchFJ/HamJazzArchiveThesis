# Filter System for Website
import csv
import glob
import json

# To find docs
output_file_path = 'Data/doc_list.json'

# Document Information
uuid = 'node_uuid'
doc_identifier = 'local_identifier'
doc_name = 'label'
labels_name = 'subject_topical'
doc_type = 'genre'

# Gives the document path in the project
def get_doc_path(doc_identifier):
    doc_path = 'Data/Transcripts/output/'
    ext = '.pdf'

    return doc_path + doc_identifier + ext

# Gets the list of labels
def get_label_list(labels_str):
    label_str = labels_str[2:len(labels_str) - 2]
    labels_list = label_str.split('},{')

    return labels_list

# Gets the documents from the CSV
def create_doc_list(json_file_path):
    doc_list = []

    with open(json_file_path, newline='') as f:
        data = json.load(f)

    for row in data:
        doc_path = get_doc_path(row[doc_identifier][2:len(row[doc_identifier]) - 2])
        label_list = get_label_list(row[labels_name])
        doc_list.append(dict(id = row[uuid], name = row[doc_name], type = row[doc_type], path = doc_path, subject_topical = label_list))

    return doc_list

def create_json(doc_list, output_file_path):
    with open(output_file_path, mode='w', newline='') as f:
        json.dump(doc_list, f, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))
    return

# CITE: https://pytutorial.com/how-to-merge-multiple-csv-files-in-python-complete-guide/
def combine_csvs():
    new_json = 'Data/Jazz_Interviews_Doc_List.json'
    doc_list = []
    csv_files = glob.glob('Data/Transcript_List/*.csv')

    with open(new_json, 'w', newline='') as output:
        for file in csv_files:
            with open(file, 'r') as input:
                reader = csv.DictReader(input)
                for row in reader:
                    doc_list.append(row)
        json.dump(doc_list, output, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))

    return

def scrape_labels(csv_path):
    new_file_name = 'Data/scraped_labels.txt'
    label_list = []

    # CITE: https://www.geeksforgeeks.org/python/create-a-new-text-file-in-python/
    with open(new_file_name, 'w') as file:
        # CITE: https://docs.python.org/3/library/csv.html
        with open(csv_path, newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                topicals = row['subject_topical']
                topicals = topicals[2:len(topicals)-2]

                topical_list = topicals.split('},{')

                for label in topical_list:
                    str_start = '"label":"'

                    label = label[len(str_start):label.find('",')]

                    if label not in label_list:
                        label_list.append(label)

            file.write("\n".join(label_list))

    return