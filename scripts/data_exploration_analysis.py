import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Enable long paths in Windows using the \\?\ prefix
data_dir = r'\\?\C:\Users\dauti\Downloads\jmh\data\jmh'

# Function to load a JSON file and return relevant data
def load_json_file(file_path):
    # Check if the file is empty
    if os.path.getsize(file_path) == 0:
        print(f"File is empty: {file_path}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
            return None
    
    primary_metric = data[0]['primaryMetric']
    
    # Extract score, scoreError, and scorePercentiles from primaryMetric
    score = primary_metric['score']
    score_error = primary_metric['scoreError']
    score_percentiles = primary_metric['scorePercentiles']
    
    return {
        'file_name': os.path.basename(file_path),  # Keep track of the file name
        'score': score,
        'score_error': score_error,
        'percentiles_0': score_percentiles['0.0'],
        'percentiles_50': score_percentiles['50.0'],
        'percentiles_90': score_percentiles['90.0'],
        'percentiles_95': score_percentiles['95.0'],
        'percentiles_99': score_percentiles['99.0']
    }

# List to store data from all JSON files
all_data = []

# Load all the JSON files in the directory
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

# Loop through all JSON files and extract relevant data
for json_file in json_files:
    file_path = os.path.join(data_dir, json_file)
    
    # Use the exact file path without modifying special characters
    data = load_json_file(file_path)
    if data:  # Only append data if it's not None
        all_data.append(data)

# Convert the list of data to a pandas DataFrame for easier analysis
df = pd.DataFrame(all_data)

# Display the first few rows of the DataFrame to verify
print(df.head())

# Save the DataFrame to a CSV file for future reference if needed
df.to_csv(r'C:\Users\dauti\Downloads\jmh\data\jmh_analysis.csv', index=False)

# Calculate basic descriptive statistics for the entire dataset
mean_score = df['score'].mean()
median_score = df['score'].median()
std_score = df['score'].std()
min_score = df['score'].min()
max_score = df['score'].max()

# Write the results to a file
with open(r'C:\Users\dauti\Downloads\jmh\data\jmh_statistics.txt', 'w') as output_file:
    output_file.write(f"Descriptive Statistics for JMH Data:\n")
    output_file.write(f"-----------------------------------\n")
    output_file.write(f"Mean Score: {mean_score}\n")
    output_file.write(f"Median Score: {median_score}\n")
    output_file.write(f"Standard Deviation of Score: {std_score}\n")
    output_file.write(f"Minimum Score: {min_score}\n")
    output_file.write(f"Maximum Score: {max_score}\n")
    output_file.write(f"-----------------------------------\n")
    output_file.write(f"Percentile Analysis:\n")
    output_file.write(f"0th Percentile (min): {df['percentiles_0'].mean()}\n")
    output_file.write(f"50th Percentile (median): {df['percentiles_50'].mean()}\n")
    output_file.write(f"90th Percentile: {df['percentiles_90'].mean()}\n")
    output_file.write(f"95th Percentile: {df['percentiles_95'].mean()}\n")
    output_file.write(f"99th Percentile: {df['percentiles_99'].mean()}\n")

# Create visualizations for the analysis
# Histogram of Scores
plt.figure(figsize=(10, 6))
plt.hist(df['score'], bins=50, color='blue', alpha=0.7)
plt.title('Distribution of Scores Across All Files')
plt.xlabel('Score (s/op)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig(r'C:\Users\dauti\Downloads\jmh\data\score_distribution.png')
plt.show()

# Scatter plot showing the scores across different files
plt.figure(figsize=(10, 6))
plt.scatter(df.index, df['score'], color='red')
plt.title('Benchmark Scores Across Different Files')
plt.xlabel('Benchmark File Index')
plt.ylabel('Score (s/op)')
plt.grid(True)
plt.savefig(r'C:\Users\dauti\Downloads\jmh\data\score_scatter_plot.png')
plt.show()

# Boxplot of Scores to understand the distribution and outliers
plt.figure(figsize=(10, 6))
plt.boxplot(df['score'])
plt.title('Boxplot of Scores Across All Files')
plt.ylabel('Score (s/op)')
plt.grid(True)
plt.savefig(r'C:\Users\dauti\Downloads\jmh\data\score_boxplot.png')
plt.show()

# Analyze Percentiles (Optional)
percentiles = ['percentiles_0', 'percentiles_50', 'percentiles_90', 'percentiles_95', 'percentiles_99']

# Plot each percentile distribution
for percentile in percentiles:
    plt.figure(figsize=(10, 6))
    plt.hist(df[percentile], bins=50, color='green', alpha=0.7)
    plt.title(f'Distribution of {percentile} Across All Files')
    plt.xlabel(f'{percentile} (s/op)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(rf'C:\Users\dauti\Downloads\jmh\data\{percentile}_distribution.png')
    plt.show()
