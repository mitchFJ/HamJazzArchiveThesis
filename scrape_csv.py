import csv

file_name = 'Jazz_Interviews - Jazz_Interviews.csv'

# CITE: https://docs.python.org/3/library/csv.html
with open(file_name, newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        labels = row['subject_topical']
        print(labels)