import csv

file_name = 'Jazz_Interviews - Jazz_Interviews.csv'
new_file_name = 'test.txt'

# CITE: https://www.geeksforgeeks.org/python/create-a-new-text-file-in-python/
with open(new_file_name, 'w') as file:
    # CITE: https://docs.python.org/3/library/csv.html
    with open(file_name, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            labels = row['subject_topical']
            file.write(labels + '\n')

print("File '{new_file_name}' created successfully.")