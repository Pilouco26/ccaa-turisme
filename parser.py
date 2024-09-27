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


def get_data():
    data = {}
    old_ccaa = ""
    count = 0
    with open('53001.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            processed_row = process_row(';'.join(row))
            # Print the second and last columns
            ccaa = processed_row[1]
            year = processed_row[-2][:4]
            if processed_row[-1] != 'Total' and year == '2023':
                tourists = int(processed_row[-1])
            else:
                continue

            count += tourists
            if (old_ccaa != ccaa):
                data[old_ccaa] = count
                old_ccaa = ccaa
                count = 0

    return data


def convert_data(data):
    regions = ['Andalucía', 'Aragón', 'Asturias', 'Balears', 'Canarias', 'Cantabria', 'Castilla - La Mancha',
               'Castilla y León', 'Cataluña', 'Ceuta', 'Comunitat Valenciana', 'Extremadura', 'Galicia', 'Madrid',
               'Melilla', 'Murcia', 'Navarra', 'País Vasco', 'Rioja']

    values = [data.get(region, 0) for region in regions]

    latitude = [37.5, 41.0, 43.3, 39.6, 28.1, 43.2, 39.9, 41.6, 41.4, 35.9, 39.5, 39.2, 42.9, 40.4, 35.3, 37.9, 42.8,
                43.0, 42.3]
    longitude = [-4.5, -1.0, -5.9, 3.0, -15.4, -3.8, -3.0, -4.7, 2.2, -5.3, -0.4, -6.3, -8.5, -3.7, -2.9, -1.1, -1.6,
                 -2.6, -2.5]

    return {
        'region': regions,
        'value': values,
        'latitude': latitude,
        'longitude': longitude
    }
# Create a DataFrame with your data
