import pandas as pd

csv_file = 'Jazz_Interviews - Jazz_Interviews.csv'

# CITE: https://www.geeksforgeeks.org/pandas/reading-specific-columns-of-a-csv-file-using-pandas/
df = pd.read_csv(csv_file, usecols=['subject_topical'])
print(df)