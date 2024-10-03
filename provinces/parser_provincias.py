import csv
import unicodedata
import re


# Function to normalize text (remove accents and special characters)
def normalize_text(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


# Process each row of the CSV
def process_row(row):
    # Handle cases where commas (e.g., in "Madrid, Comunidad de") should not be split
    # Join any consecutive fields that may have been incorrectly split by a comma in the region/province names
    columns = row.split(';')
    print(columns)

    # Replace empty values with "-" and set Total to 0 if it's empty
    processed_row = [col.strip() if col else "-" for col in columns]
    if not processed_row[-1] or processed_row[-1] in ['""', '.']:
        processed_row[-1] = 0
    else:
        # Check if the value is a valid number after removing periods
        cleaned_value = processed_row[-1].replace('.', '')
        if cleaned_value.isdigit():
            processed_row[-1] = int(cleaned_value)
        else:
            processed_row[-1] = 0
    return processed_row


# Main function to get data and save
def get_data_and_save():
    data = {}
    old_provincia = ""
    count = 0

    with open('../data/cleaned_53000.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            processed_row = process_row(';'.join(row))
            print(processed_row)
            provincia = processed_row[3]
            year = processed_row[-2][:4]

            print(provincia)
            # Only process rows for the year 2023 and valid tourist numbers
            if processed_row[-1] != 'Total' and year == '2023':
                tourists = int(processed_row[-1])
                count += tourists
                # When the region changes, save the count for the old region
                if old_provincia != provincia:
                    if old_provincia and old_provincia != '-':  # Ensure old_provincia is not empty or invalid
                        data[old_provincia] = count  # Save the tourist count for the previous region
                    old_provincia = provincia  # Update old_provincia to the current region
                    count = 0  # Reset the count for the new region


    # Save the data into a text file
    with open('data_provincia.txt', mode='w', encoding='utf-8') as f:
        for provincia, tourists in data.items():
            f.write(f"{provincia}: {tourists}\n")


# Run the function to process and save data
get_data_and_save()
