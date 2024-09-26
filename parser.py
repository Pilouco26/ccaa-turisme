import csv

import pandas as pd


def process_row(row):
    # Split the row by semicolons
    columns = row.split(';')

    # Ensure the row has exactly 7 columns
    while len(columns) < 7:
        columns.append("-")

    # Replace empty values with "-" and set Total to 0 if it's empty
    processed_row = [col if col else "-" for col in columns]
    if not processed_row[-1] or pd.isna(processed_row[-1]) or processed_row[-1] in ['""', '.']:
        processed_row[-1] = 0
    else:
        # Check if the value is a valid number after removing periods
        cleaned_value = processed_row[-1].replace('.', '')
        if cleaned_value.isdigit():
            processed_row[-1] = int(cleaned_value)
        else:
            processed_row[-1] = 0  # or handle it in another way if needed
    return processed_row


old_ccaa = ""
count = 0
with open('53001.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        processed_row = process_row(';'.join(row))
        # Print the second and last columns
        ccaa = processed_row[1]
        if (processed_row[-1] != 'Total'):
            tourists = int(processed_row[-1])
        else:
            continue

        count += tourists
        if (old_ccaa != ccaa):
            print(ccaa, count)
            old_ccaa = ccaa
            count = 0
