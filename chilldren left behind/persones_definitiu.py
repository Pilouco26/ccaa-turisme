import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Initialize lists to store names and values
names = []
values = []

# Load the data from the file
with open('../data_tourism', 'r', encoding='utf-8') as file:
    for line in file:
        # Split each line into name and value using ':' as the delimiter
        name, value = line.strip().split(': ')
        names.append(name)
        values.append(int(value))  # Convert value to integer

# Create the DataFrame from the lists
data = pd.DataFrame({'name': names, 'value': values})

# Calculate total value
total = data['value'].sum()

# Calculate percentages and store them in a dictionary
percentages = {row['name']: (row['value'] / total) * 100 for _, row in data.iterrows()}

# Define the paths to the flags (make sure these paths are correct)
flag_paths = {
    'Andalucía': 'flags/Andalucía.png',
    'Aragón': 'flags/Aragón.png',
    'Asturias': 'flags/Asturias.png',
    'Balears': 'flags/Balears.png',
    'Canarias': 'flags/Canarias.png',
    'Cantabria': 'flags/Cantabria.png',
    'Castilla - La Mancha': 'flags/Castilla - La Mancha.png',
    'Castilla y León': 'flags/Castilla y León.png',
    'Cataluña': 'flags/Cataluña.png',
    'Ceuta': 'flags/Ceuta.png',
    'Comunitat Valenciana': 'flags/Comunitat Valenciana.png',
    'Extremadura': 'flags/Extremadura.png',
    'Galicia': 'flags/Galicia.png',
    'Madrid': 'flags/Madrid.png',
    'Melilla': 'flags/Melilla.png',
    'Murcia': 'flags/Murcia.png',
    'Navarra': 'flags/Navarra.png',
    'País Vasco': 'flags/País Vasco.png',
    'Rioja': 'flags/Rioja.png'
}

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each region with the corresponding number of flags
for i, (region, percent) in enumerate(percentages.items()):
    num_flags = int(percent)  # Each flag represents 1%
    flag_path = flag_paths.get(region)  # Get flag path for the region

    for j in range(num_flags):
        # Calculate positions for the flags
        x_pos = j % 10  # Position across the x-axis (10 flags per row)
        y_pos = i + (j // 10) * 0.3  # Adjust y position for rows of flags

        # Display the flag
        if flag_path:  # Ensure the flag path exists
            img = mpimg.imread(flag_path)
            # Set extents for flags (300x200 pixels)
            ax.imshow(img, extent=(x_pos - 0.75, x_pos + 0.75, y_pos - 0.5, y_pos + 0.5), aspect='auto')

# Remove axis
ax.axis('off')

# Add the title
plt.title("Si hubiera 100 turistas en España, visitarían...", fontsize=14)

# Show the plot
plt.tight_layout()
plt.show()




