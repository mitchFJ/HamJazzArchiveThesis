# Filters out the document list
def check_list(doc_list, new_doc_list, label_list, is_included):
    # Checks through each doc to see if a label is in the doc_list
    for doc in doc_list:
        # CITE: https://www.geeksforgeeks.org/python/python-test-if-string-contains-element-from-list/
        if any(label in doc['subject_topical'] for label in label_list):
            if is_included:
                new_doc_list.append(doc)
        else:
            if not is_included:
                new_doc_list.append(doc)
    return

# Checks to see if there are any filters active in the documents
def filter_docs(doc_list, include_list, exclude_list):
    new_doc_list = []

    # Checks if both filter lists have no elements
    if len(include_list) < 1 and len(exclude_list) < 1:
        new_doc_list = doc_list
        return new_doc_list

    # Check if documents have include filters
    if len(include_list) >= 1:
        check_list(doc_list, new_doc_list, include_list, True)
    
    # Check if documents have exclude filters
    if len(exclude_list) >= 1:
        check_list(doc_list, new_doc_list, exclude_list, False)
    
    return new_doc_list