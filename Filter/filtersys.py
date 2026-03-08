# Filter System for Website
import csv

include_list = ["composers"]
exclude_list = ["jazz"]

doc_list = []
file_name = 'Jazz_Interviews - Jazz_Interviews.csv'

with open(file_name, newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    if len(include_list) > 0:
        print("Has Include Filters")

        for row in csv_reader:
            for label in include_list:
                label = '"label":"' + label + '"'

                if label in row['subject_topical']:
                    doc_list.append(dict(name = row['label'], labels = row['subject_topical']))
    else:
        print("No Include Filters")

        for row in csv_reader:
            doc_list.append(dict(name = row['label'], labels = row['subject_topical']))

# Exclude Filters not Working (Why is it no finding the Jazz label in all the docs?)
# Registers it as a string
if len(exclude_list) > 0:
    print("Has Exclude Filters")
    i = 0

    for row in doc_list:
        for label in exclude_list:
            label = '"label":"' + label + '"'
            if label in row['labels']:
                doc_list.pop(i)
        i += 1
else:
    print("No Exclusionary Filters")

print(len(doc_list))
# for row in doc_list:
#     print(row['name'] + " " + row['labels'])