# Scrapes Subject Topicals column of the CSV file

# Notes: Improve efficiency of scrape

import csv

file_path = 'Utilities/Jazz_Interviews - Jazz_Interviews.csv'
new_file_name = 'scraped_labels.txt'

label_list = []

# CITE: https://www.geeksforgeeks.org/python/create-a-new-text-file-in-python/
with open(new_file_name, 'w') as file:
    # CITE: https://docs.python.org/3/library/csv.html
    with open(file_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            topicals = row['subject_topical']
            topicals = topicals[2:len(topicals)-2]

            topical_list = topicals.split('},{')

            for label in topical_list:
                str_start = '"label":"'

                label = label[len(str_start):]
                label = label[:label.find('"')]

                if label not in label_list:
                    label_list.append(label)

        file.write("\n".join(label_list))

print(f"File '{new_file_name}' created successfully.")