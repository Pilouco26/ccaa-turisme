import csv

# Define the input and output file names
input_file = '../data/53000.csv'
output_file = '../data/cleaned_53000.csv'

# Open the input file and output file
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Loop through each row in the input file
    for row in reader:
        # Check if the row starts with 'Total Nacional;Total Nacional;'
        if row[0] == 'Total Nacional' and row[1] == 'Total Nacional':
            # Write the row to the output file
            writer.writerow(row)

print(f"Cleaned data has been saved to {output_file}")
