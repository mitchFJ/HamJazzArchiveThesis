# Filter System for Website

include_list = []
exclude_list = []

doc_list = []

if len(include_list) > 1:
    print("Has Include Filters")
else:
    print("Does not have Include Filters")

if len(exclude_list) > 1:
    print("Has Exclude Filters")
else:
    print("Does not have Exclude Filters")