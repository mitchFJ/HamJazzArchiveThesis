import json

labels_name = 'subject_topical'

# Scrapes Labels from the generated Doc List JSON
def scrape_labels(doc_list_path = 'Data/doc_list.json'):
    new_file_name = 'Data/scraped_labels.txt'
    label_list = []

    with open(doc_list_path, newline='') as list_file:
        data = json.load(list_file)

        for doc in data.values():
            missing_labels = list(set(doc[labels_name]) - set(label_list))
            label_list.extend(missing_labels)

    with open(new_file_name, 'w') as file:
        file.write("\n".join(label_list))

    return

scrape_labels()