import csv

def process_row(row):
    # Split the row by semicolons
    columns = row.split(';')

    # Ensure the row has exactly 7 columns
    while len(columns) < 7:
        columns.append("-")

    # Replace empty values with "-" and set Total to 0 if it's empty
    processed_row = [col if col else "-" for col in columns]
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

def get_data_and_save():
    data = {}
    old_ccaa = ""
    count = 0
    with open('53001.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            processed_row = process_row(';'.join(row))
            # Get the necessary columns
            ccaa = processed_row[1]
            year = processed_row[-2][:4]

            # Only process rows for the year 2022 and valid tourist numbers
            if processed_row[-1] != 'Total' and year == '2023':
                tourists = int(processed_row[-1])
            else:
                continue

            count += tourists

            # When the region changes, save the count for the old region
            if old_ccaa != ccaa:
                if old_ccaa and old_ccaa != '-':  # Ensure old_ccaa is not empty or invalid
                    data[old_ccaa] = count  # Save the tourist count for the previous region
                old_ccaa = ccaa  # Update old_ccaa to the current region
                count = 0  # Reset the count for the new region

        # Ensure the last region is added to the data dictionary if valid
        if ccaa and ccaa != '-':
            data[ccaa] = count

    # Save the data into a text file
    with open('data_tourism.txt', mode='w', encoding='utf-8') as f:
        for ccaa, tourists in data.items():
            f.write(f"{ccaa}: {tourists}\n")

# Run the function to process and save data
get_data_and_save()
