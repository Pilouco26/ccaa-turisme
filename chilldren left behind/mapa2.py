import os

import matplotlib.pyplot as plt

from espanya.visualize import plot_data_map


def calculate_tourists_per_habitant(tourists_data, habitants_data):
    tourists_per_habitant = {}
    for region in tourists_data:
        if region in habitants_data and habitants_data[region] != 0:
            tourists_per_habitant[region] = tourists_data[region] / habitants_data[region]
        else:
            tourists_per_habitant[region] = None  # Handle division by zero or missing habitants data
    return tourists_per_habitant


def load_data_from_file(file):
    source = {}
    with open(file, mode='r', encoding='utf-8') as file:
        for line in file:
            # Each line has the format: "ccaa: tourists"
            ccaa, tourists = line.strip().split(': ')
            source[ccaa] = int(tourists)  # Convert tourists to an integer
    return source





print("getting data...")
# Load the data into the dictionary
data = load_data_from_file('../data/data_tourism')
habitants = load_data_from_file('data_superficie')
print("data fetched")

# Calculate the ratio of tourists per habitant
tourists_per_habitant = calculate_tourists_per_habitant(data, habitants)



# Calculate the region with the maximum number of tourists
max_region = max(tourists_per_habitant, key=tourists_per_habitant.get)  # Get the region with the max tourists

max_value = tourists_per_habitant[max_region]  # Get the max number of tourists
print(max_region, max_value)

plot_data_map(tourists_per_habitant, max_value)
os.startfile('spain_map.png')
# Close the plot to avoid display in interactive environments
plt.close()
