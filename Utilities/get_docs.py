# Filter System for Website
import csv
import glob

# To find docs
csv_file_paths = ['Data/Transcript_List/Jazz_Interviews - Jazz_Interviews.csv', 'Data/Trasncript_List/Jazz_Interviews_Transcript_only - Jazz_Interviews_Transcript_only.csv']

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

    print(f"File path created successfully.")

    return doc_path + doc_identifier + ext

# Gets the list of labels
def get_label_list(labels_str):
    label_str = labels_str[2:len(labels_str) - 2]
    labels_list = label_str.split('},{')

    print(f"Labels turned into list successfully.")

    return labels_list

# Gets the documents from the CSV
def get_docs_from_csv(csv_file_path):
    doc_list = []

    with open(csv_file_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        i = 0

        for row in csv_reader:
            doc_path = get_doc_path(row[doc_identifier][2:len(row[doc_identifier]) - 2])
            label_list = get_label_list(row[labels_name])
            doc_list.append(dict(index = i, id = row[uuid], name = row[doc_name], type = row[doc_type], path = doc_path, subject_topical = label_list))

            i += 1

    print(f"Docs from '{csv_file_path}' obtained successfully.")

    return doc_list

# CITE: https://pytutorial.com/how-to-merge-multiple-csv-files-in-python-complete-guide/
def combine_csvs():
    new_csv = 'Data/Jazz_Interviews_Doc_List.csv'
    csv_files = glob.glob('Data/Transcript_List/*.csv')

    # CITE: https://blog.finxter.com/5-best-ways-to-retrieve-the-first-row-from-a-csv-in-python/
    with open(csv_files[0], 'r') as f:
        headers = next(csv.reader(f))

    with open(new_csv, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        
        for file in csv_files:
            with open(file, 'r') as input:
                reader = csv.reader(input)
                next(reader)
                for row in reader:
                    writer.writerow(row)

    print(f"Files '{csv_file_paths}' combined successfully.")

    return csv_files

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
                    # CITE: https://stackoverflow.com/questions/1549641/how-can-i-capitalize-the-first-letter-of-each-word-in-a-string
                    label = ' '.join(word[0].upper() + word[1:] for word in label.split())

                    if label not in label_list:
                        label_list.append(label)

            file.write("\n".join(label_list))

    print(f"File '{new_file_name}' created successfully.")