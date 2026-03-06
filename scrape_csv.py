import csv
import re

file_name = 'Jazz_Interviews - Jazz_Interviews.csv'
new_file_name = 'test.txt'

# CITE: https://www.geeksforgeeks.org/python/create-a-new-text-file-in-python/
with open(new_file_name, 'w') as file:
    # CITE: https://docs.python.org/3/library/csv.html
    with open(file_name, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            labels = row['subject_topical']
            labels = labels[2:len(labels)-2]

            file.write(labels + '\n')

print(f"File '{new_file_name}' created successfully.")