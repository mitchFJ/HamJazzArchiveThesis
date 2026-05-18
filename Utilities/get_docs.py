# Filter System for Website
import csv
import glob
import json
import re

# To find docs
output_file_path = 'Data/doc_list.json'

# Document Information
uuid = 'node_uuid'
doc_identifier = 'local_identifier'
doc_name = 'label'
labels_name = 'subject_topical'
doc_type = 'genre'

# Generates a doc object to compile necessary doc information
class Doc:
    def __init__(self, uuid, doc_name, doc_type, doc_path, label_list):
        self.id = uuid
        self.name = doc_name
        self.type = doc_type
        self.path = doc_path
        self.subject_topical = label_list
        pass

# Gives the document path in the project
def get_doc_path(doc_identifier):
    directory_path = 'Data/Transcripts/output/'
    ext = '.pdf'

    return directory_path + doc_identifier + ext

# Gets the list of labels
def get_label_list(labels_str):
    # Cleans up the string to get the labels
    cut_start = labels_str.index('\":\"') + len('\":\"')
    cut_end = re.search(r'\",\"uri\":\"[^"]*\"}]', labels_str).start()
    labels_str = labels_str[cut_start:cut_end]
    
    # Splits string to get individual labels
    labels_list = re.split(r'\",\"uri\":\"[^"]*\"},{\"label\":\"', labels_str)

    return labels_list

# Combines Transcript information from CSV files into one dictionary
def combine_csvs():
    doc_list = []
    csv_files = glob.glob('Data/Transcript_List/*.csv')

    for file in csv_files:
        with open(file, 'r') as input:
            reader = csv.DictReader(input)
            for row in reader:
                doc_list.append(row)

    return doc_list

# Creates a JSON file for the Doc List
def create_json(doc_list, output_file_path):
    with open(output_file_path, mode='w', newline='') as f:
        json.dump(doc_list, f, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))
    return

# Creates a doc list JSON file for other programs to reference from
def create_doc_list():
    doc_list = {}
    data = combine_csvs()

    for row in data:
        doc_path = get_doc_path(row[doc_identifier][2:len(row[doc_identifier]) - 2])
        label_list = get_label_list(row[labels_name])
        doc_list = {**doc_list, doc_path: Doc(row[uuid], row[doc_name], row[doc_type], doc_path, label_list).__dict__}

    create_json(doc_list, output_file_path)

    return