import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Directory where the JSON files are stored
data_dir = r'C:\Users\dauti\Downloads\jmh\data\jmh'

# File to write output for report
output_file_path = r'C:\Users\dauti\Downloads\jmh\data\jmh_jdk_analysis.txt'
output_file = open(output_file_path, 'w')

# Function to load JSON file and extract relevant data
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    primary_metric = data[0]['primaryMetric']
    jdk_version = data[0].get('jdkVersion', 'Unknown')  # Extract JDK version, defaulting to 'Unknown' if missing
    return primary_metric, jdk_version

# List to store data for comparison
all_data = []

# Iterate over all JSON files to extract performance data and JDK version
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

for json_file in json_files:
    file_path = os.path.join(data_dir, json_file)
    try:
        metric_data, jdk_version = load_json_file(file_path)

        # Extract relevant performance metrics
        score = metric_data['score']
        score_error = metric_data['scoreError']
        score_percentiles = metric_data['scorePercentiles']

        all_data.append({
            'file_name': os.path.basename(file_path),
            'jdk_version': jdk_version,
            'score': score,
            'score_error': score_error,
            'percentile_50': score_percentiles['50.0'],
            'percentile_90': score_percentiles['90.0'],
            'percentile_99': score_percentiles['99.0']
        })
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

# Convert data into a pandas DataFrame
df = pd.DataFrame(all_data)

# Group data by JDK version
grouped = df.groupby('jdk_version')

# Write results to the output file
output_file.write("JDK Performance Variability Analysis\n")
output_file.write("--------------------------------------------------------------\n")

# Iterate over each JDK version and calculate descriptive statistics
for jdk_version, group in grouped:
    output_file.write(f"\nJDK Version: {jdk_version}\n")
    output_file.write(f"Number of Benchmarks: {len(group)}\n")
    output_file.write(f"Mean Score: {group['score'].mean()}\n")
    output_file.write(f"Median Score: {group['score'].median()}\n")
    output_file.write(f"Standard Deviation of Score: {group['score'].std()}\n")
    output_file.write(f"Mean 50th Percentile: {group['percentile_50'].mean()}\n")
    output_file.write(f"Mean 90th Percentile: {group['percentile_90'].mean()}\n")
    output_file.write(f"Mean 99th Percentile: {group['percentile_99'].mean()}\n")
    
    # Visualize score distribution for each JDK version
    plt.figure(figsize=(10, 6))
    plt.hist(group['score'], bins=50, alpha=0.7, label=f'JDK {jdk_version}')
    plt.title(f'Score Distribution for JDK {jdk_version}')
    plt.xlabel('Score (s/op)')
    plt.ylabel('Frequency')
    plt.legend()
    plot_file = rf'C:\Users\dauti\Downloads\jmh\data\jdk_{jdk_version}_score_distribution.png'
    plt.savefig(plot_file)
    plt.close()
    
    output_file.write(f"Score distribution plot saved to: {plot_file}\n")

output_file.write("\nEnd of JDK Performance Variability Analysis\n")
output_file.close()
