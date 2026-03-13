import matplotlib.pyplot as plt

# Sample data
categories = ['najam', 'polupansion', 'all inclusive', 'nocenje s doruckom']
values = [10439, 845, 83, 243]

# Calculate total for percentage
total = sum(values)

# Create a bar graph
plt.bar(categories, values)

# Add title and labels
plt.title('Sample Bar Graph')
plt.xlabel('Categories')
plt.ylabel('Values')

# Add value and percentage labels on each bar
for i, v in enumerate(values):
    percentage = (v / total) * 100
    label = f'{v} ({percentage:.1f}%)'
    plt.text(i, v + max(values) * 0.02, label, ha='center', va='bottom')

# Show the plot
plt.show()