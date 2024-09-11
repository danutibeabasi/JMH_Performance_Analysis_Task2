# import os
# import json
# import numpy as np
# import matplotlib.pyplot as plt

# # Directory where the JSON files are stored
# data_dir = r'C:\Users\dauti\Downloads\jmh\data\jmh'

# # File to write output for report
# output_file_path = r'C:\Users\dauti\Downloads\jmh\data\jmh_replication_output.txt'
# output_file = open(output_file_path, 'w')

# # Function to load JSON file and extract relevant data
# def load_json_file(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     primary_metric = data[0]['primaryMetric']
#     return primary_metric

# # Changepoint detection (Simulated by analyzing performance fluctuation)
# def detect_changepoints(data):
#     # A simple change detection based on significant performance shifts
#     mean_changes = np.diff(np.mean(data, axis=0))  # difference in means
#     significant_shifts = np.where(np.abs(mean_changes) > 0.05)[0]  # adjust the threshold based on sensitivity
#     return significant_shifts

# # Select a few benchmark files for analysis
# json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

# output_file.write("Replication of Study: Steady-State Performance and Warmup Estimation\n")
# output_file.write("--------------------------------------------------------------\n")

# for json_file in json_files[:5]:  # Select 5 files for replication
#     file_path = os.path.join(data_dir, json_file)
#     metric_data = load_json_file(file_path)

#     # Extract performance metrics from rawDataHistogram
#     raw_data = metric_data['rawDataHistogram'][0]
    
#     # Ensure that raw_data is a list of lists and extract the first value (execution time)
#     execution_times = [item[0] for item in raw_data if isinstance(item, list) and len(item) > 0]

#     # Apply changepoint detection
#     execution_times_array = np.array(execution_times)
#     changepoints = detect_changepoints(execution_times_array)
    
#     # Write results to the output file
#     output_file.write(f"\nBenchmark File: {json_file}\n")
#     output_file.write(f"Developer-defined Warmup Iterations: {metric_data.get('warmupIterations', 0)}\n")
#     output_file.write(f"Detected Changepoints (Significant Shifts in Performance): {changepoints}\n")
    
#     # Plot the performance data with detected changepoints
#     plt.plot(execution_times_array, label="Performance Over Iterations")
#     for point in changepoints:
#         plt.axvline(x=point, color='r', linestyle='--', label="Detected Changepoint")
#     plt.title(f"Benchmark Performance - {json_file}")
#     plt.xlabel('Iterations')
#     plt.ylabel('Execution Time (s/op)')
#     plt.legend()
#     plot_file = rf'C:\Users\dauti\Downloads\jmh\data\{json_file}_performance_plot.png'
#     plt.savefig(plot_file)
#     plt.close()
    
#     # Write the plot reference to the file
#     output_file.write(f"Performance plot saved to: {plot_file}\n")

# output_file.write("\nEnd of Replication Study\n")
# output_file.close()


import os
import json
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt

# Directory where the JSON files are stored
data_dir = r'C:\Users\dauti\Downloads\jmh\data\jmh'

# File to write output for report
output_file_path = r'C:\Users\dauti\Downloads\jmh\data\jmh_replication_output_pelt.txt'
output_file = open(output_file_path, 'w')

# Function to load JSON file and extract relevant data
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    primary_metric = data[0]['primaryMetric']
    return primary_metric

# Changepoint detection using the PELT algorithm
def detect_changepoints(data):
    model = "l2"  # Using L2 cost function, as in the study
    algo = rpt.Pelt(model=model, min_size=3, jump=1).fit(data)
    result = algo.predict(pen=10)  # Penalty chosen for detection sensitivity, can be tuned
    return result

# Select a few benchmark files for analysis
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

output_file.write("Replication of Study: Steady-State Performance and Warmup Estimation using PELT\n")
output_file.write("--------------------------------------------------------------\n")

for json_file in json_files[:5]:  # Select 5 files for replication
    file_path = os.path.join(data_dir, json_file)
    metric_data = load_json_file(file_path)

    # Extract performance metrics from rawDataHistogram
    raw_data = metric_data['rawDataHistogram'][0]
    
    # Ensure that raw_data is a list of lists and extract the first value (execution time)
    execution_times = [item[0] for item in raw_data if isinstance(item, list) and len(item) > 0]

    # Apply changepoint detection using PELT
    execution_times_array = np.array(execution_times)
    changepoints = detect_changepoints(execution_times_array)
    
    # Write results to the output file
    output_file.write(f"\nBenchmark File: {json_file}\n")
    output_file.write(f"Developer-defined Warmup Iterations: {metric_data.get('warmupIterations', 0)}\n")
    output_file.write(f"Detected Changepoints (Significant Shifts in Performance): {changepoints}\n")
    
    # Plot the performance data with detected changepoints
    plt.plot(execution_times_array, label="Performance Over Iterations")
    for point in changepoints:
        plt.axvline(x=point, color='r', linestyle='--', label="Detected Changepoint")
    plt.title(f"Benchmark Performance - {json_file}")
    plt.xlabel('Iterations')
    plt.ylabel('Execution Time (s/op)')
    plt.legend()
    plot_file = rf'C:\Users\dauti\Downloads\jmh\data\{json_file}_performance_plot_pelt.png'
    plt.savefig(plot_file)
    plt.close()
    
    # Write the plot reference to the file
    output_file.write(f"Performance plot saved to: {plot_file}\n")

output_file.write("\nEnd of Replication Study using PELT\n")
output_file.close()
