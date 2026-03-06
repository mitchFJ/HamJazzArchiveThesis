import csv

file_name = 'Jazz_Interviews - Jazz_Interviews.csv'
new_file_name = 'test.txt'

# CITE: https://www.geeksforgeeks.org/python/create-a-new-text-file-in-python/
with open(new_file_name, 'w') as file:
    # CITE: https://docs.python.org/3/library/csv.html
    with open(file_name, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            topicals = row['subject_topical']
            topicals = topicals[2:len(topicals)-2]

            topical_list = topicals.split('},{')

            for label in topical_list:
                str_start = '"label":"'
                str_end = '","uri":""'

                label = label[len(str_start):len(label)-len(str_end)]

                file.write(label + '\n')

print(f"File '{new_file_name}' created successfully.")